#!/usr/bin/env python3
"""Build and verify fighter voice-line transcripts for local browser review.

This tool uses the project's existing real voice clips as sources.  It never
creates replacement speech with TTS or another speaker.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Optional

import imageio_ffmpeg

try:
    import yt_dlp
except ImportError:
    yt_dlp = None

ROOT = Path(__file__).resolve().parent.parent
VOICE_JSON = ROOT / "public" / "assets" / "voice-lines.json"
PUBLIC_DIR = ROOT / "public"
LANGUAGES = ("ta", "te", "ml", "hi", "en")
LIMITS = {
    "bark": 1.2,
    "special": 1.8,
    "intro": 3.0,
    "win": 3.0,
    "super": 3.5,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Transcribe and verify fighter voice lines")
    parser.add_argument("--cache-dir", default=".audio_cache", help="Transcript and audio cache directory")
    parser.add_argument("--fighters", default="", help="Comma-separated fighter IDs (default: all)")
    parser.add_argument("--whisper-model", default="small", help="faster-whisper model name")
    parser.add_argument("--dry-run", action="store_true", help="Inspect sources and cache without downloading/transcribing")
    return parser.parse_args()


def normalized_words(text: str) -> List[str]:
    import re
    return re.findall(r"[^\W\d_]+(?:['-][^\W\d_]+)*", text.lower(), flags=re.UNICODE)


def match_score(expected: str, actual: str) -> float:
    expected_words = normalized_words(expected)
    actual_words = normalized_words(actual)
    if not expected_words:
        return 1.0 if not actual_words else 0.0
    if not actual_words:
        return 0.0
    # SequenceMatcher rewards the order of the actual spoken words.
    from difflib import SequenceMatcher
    joined_expected = " ".join(expected_words)
    joined_actual = " ".join(actual_words)
    return round(SequenceMatcher(None, joined_expected, joined_actual).ratio(), 3)


def audio_path(source: str) -> Optional[Path]:
    if not source:
        return None
    if source.startswith("/"):
        source = source[1:]
    path = PUBLIC_DIR / source
    return path if path.is_file() else None


def duration_limit(line_id: str) -> Optional[float]:
    if line_id.startswith("bark"):
        return LIMITS["bark"]
    if line_id.startswith("special"):
        return LIMITS["special"]
    for kind in ("intro", "win", "super"):
        if line_id == kind:
            return LIMITS[kind]
    return None


def ffprobe_duration(path: Path) -> Optional[float]:
    ffprobe = str(Path(imageio_ffmpeg.get_ffmpeg_exe()).with_name("ffprobe.exe"))
    if not Path(ffprobe).is_file():
        ffprobe = "ffprobe"
    try:
        result = subprocess.run(
            [ffprobe, "-v", "error", "-show_entries", "format=duration", "-of", "json", str(path)],
            capture_output=True,
            text=True,
            timeout=15,
        )
        if result.returncode == 0:
            return float(json.loads(result.stdout)["format"]["duration"])
    except Exception:
        pass
    return None


def transcribe(path: Path, model_name: str, cache_dir: Path) -> Dict:
    digest = hashlib.sha256(f"{path.resolve()}|{model_name}".encode("utf-8")).hexdigest()[:20]
    cache_file = cache_dir / "transcripts" / f"{digest}.json"
    if cache_file.is_file():
        return json.loads(cache_file.read_text(encoding="utf-8"))
    try:
        from faster_whisper import WhisperModel
    except Exception as exc:
        return {"whisperText": "", "words": [], "language": "", "error": f"faster-whisper unavailable: {exc}"}

    model = WhisperModel(model_name, device="auto", compute_type="auto")
    best = None
    best_segments = []
    for language in LANGUAGES:
        segments, info = model.transcribe(
            str(path),
            language=language,
            word_timestamps=True,
            vad_filter=True,
        )
        segment_list = list(segments)
        text = " ".join(segment.text.strip() for segment in segment_list).strip()
        candidate = {"text": text, "segments": segment_list, "language": info.language, "probability": info.language_probability}
        if best is None or candidate["probability"] > best["probability"]:
            best = candidate
            best_segments = segment_list

    words = []
    for segment in best_segments:
        for word in getattr(segment, "words", []) or []:
            words.append({"word": word.word.strip(), "start": word.start, "end": word.end})
    result = {
        "whisperText": best["text"] if best else "",
        "words": words,
        "language": best["language"] if best else "",
        "languageProbability": round(best["probability"], 4) if best else 0.0,
    }
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    cache_file.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


def cut_and_normalize(source: Path, destination: Path, maximum: float) -> bool:
    destination.parent.mkdir(parents=True, exist_ok=True)
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    duration = ffprobe_duration(source)
    if duration is not None and duration > maximum:
        cut_duration = maximum
    else:
        cut_duration = duration
    args = [ffmpeg, "-y", "-hide_banner", "-loglevel", "error"]
    args += ["-i", str(source)]
    if cut_duration is not None:
        args += ["-t", f"{cut_duration:.3f}"]
    args += ["-af", "loudnorm=I=-14:TP=-1.2:LRA=9", "-ar", "44100", "-ac", "2", str(destination)]
    return subprocess.run(args, capture_output=True).returncode == 0


def process_voice_lines(data: Dict, fighter_ids: Iterable[str], cache_dir: Path, model_name: str, dry_run: bool) -> tuple[Dict, List[Dict]]:
    selected = set(fighter_ids)
    rows = []
    updated = json.loads(json.dumps(data))

    for fighter, lines in updated.items():
        if selected and fighter not in selected:
            continue
        reference = next(
            (entry.get("audio") for line_id, entry in lines.items()
             if isinstance(entry, dict) and entry.get("audio")),
            None,
        )
        reference_file = audio_path(reference)
        for line_id, entry in lines.items():
            if not isinstance(entry, dict):
                continue
            source = entry.get("audio", "")
            source_file = audio_path(source)
            missing = source_file is None
            if missing and reference_file is not None:
                source_file = reference_file
                entry["source"] = "missing-original/reference"
            elif source_file is not None:
                entry["source"] = source

            maximum = duration_limit(line_id)
            entry.setdefault("approved", False)
            entry.setdefault("whisperText", "")
            entry.setdefault("matchScore", 0.0)
            entry.setdefault("speakerScore", 0.0)

            if dry_run:
                entry["source"] = entry.get("source") or ("missing-source" if missing else source)
                rows.append({
                    "fighter": fighter,
                    "line": line_id,
                    "source": entry["source"],
                    "match": entry["matchScore"],
                    "speaker": entry["speakerScore"],
                    "missing": missing,
                })
                continue

            if source_file is None:
                rows.append({"fighter": fighter, "line": line_id, "source": "missing", "match": entry["matchScore"], "speaker": entry["speakerScore"], "missing": True})
                continue

            cache_clip = cache_dir / "clips" / fighter / f"{line_id}.mp3"
            ok = cut_and_normalize(source_file, cache_clip, maximum or 10.0)
            entry["durationLimit"] = maximum
            if not ok:
                rows.append({"fighter": fighter, "line": line_id, "source": entry["source"], "match": 0.0, "speaker": entry["speakerScore"], "missing": False})
                continue

            transcript = transcribe(cache_clip, model_name, cache_dir)
            whisper_text = transcript.get("whisperText", "")
            entry["whisperText"] = whisper_text
            entry["matchScore"] = match_score(entry.get("text", ""), whisper_text)
            entry["speakerScore"] = 0.0
            if "error" in transcript:
                entry["transcriptError"] = transcript["error"]
            rows.append({
                "fighter": fighter,
                "line": line_id,
                "source": entry["source"],
                "match": entry["matchScore"],
                "speaker": entry["speakerScore"],
                "missing": False,
            })
    return updated, rows


def print_summary(rows: List[Dict]) -> None:
    print(f"{'FIGHTER':12} {'LINE':10} {'STATUS':16} {'MATCH':>6} {'SPEAKER':>8}")
    print("-" * 58)
    bad = 0
    for row in rows:
        statuses = []
        if row["missing"]:
            statuses.append("missing")
        if row["match"] < 0.75:
            statuses.append("match<0.75")
        if row["speaker"] < 0.70:
            statuses.append("speaker<0.70")
        status = ", ".join(statuses) or "ok"
        bad += bool(statuses)
        print(f"{row['fighter']:12} {row['line']:10} {status:16} {row['match']:6.3f} {row['speaker']:8.3f}")
    print(f"\n{bad} line(s) need review")


def main() -> int:
    args = parse_args()
    cache_dir = (ROOT / args.cache_dir).resolve() if not os.path.isabs(args.cache_dir) else Path(args.cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    fighter_ids = [value.strip() for value in args.fighters.split(",") if value.strip()]

    if not VOICE_JSON.is_file():
        print(f"Missing voice-lines file: {VOICE_JSON}", file=sys.stderr)
        return 1
    data = json.loads(VOICE_JSON.read_text(encoding="utf-8"))
    updated, rows = process_voice_lines(data, fighter_ids, cache_dir, args.whisper_model, args.dry_run)

    if not args.dry_run:
        tmp = VOICE_JSON.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(updated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        os.replace(tmp, VOICE_JSON)
    print_summary(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
