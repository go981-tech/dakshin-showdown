#!/usr/bin/env python3
"""Build and verify real fighter voice clips without TTS or speaker substitution."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from difflib import SequenceMatcher
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

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

# Curated solo dialogue targets.  Search queries are deliberately distinct:
# no montage, compilation, dubbed, or mixed-cast source is accepted.
ICONIC_DIALOGUE_TARGETS = {
    "modi": {
        "intro": ("Tamilnattu arasin mudhalamaichararga?", ["Stalin Tamil Nadu chief minister speech", "Stalin Tamil political speech"]),
        "special1": ("Tamilnattu arasin mudhalamaichararga?", ["Stalin Tamil Nadu Chief Minister original speech"]),
        "special2": ("Nermaiyaga seyven endrum urudhi mozhigiren", ["Stalin Tamil Nadu oath promise speech"]),
        "super": ("Muthuvel Karunanidhi Stalin Vidiyal Aatchi", ["Stalin Tamil Nadu Vidiyal Aatchi speech"]),
        "win": ("Nermaiyaga seyven endrum urudhi mozhigiren", ["Stalin speech Tamil urudhi mozhigiren"]),
        "bark1": ("Tamilnattu arasin mudhalamaichararga?", ["Stalin Tamil Nadu address"]),
        "bark2": ("Nermaiyaga seyven endrum urudhi mozhigiren", ["Stalin Tamil oath speech"]),
    },
    "rahul": {
        "intro": ("What bro? It's very wrong bro!", ["Vijay what bro Tamil interview", "Vijay Leo brother interview"]),
        "special1": ("What bro? It's very wrong bro!", ["Vijay Leo brother interview speech"]),
        "special2": ("En nenjil kudiyirukkum", ["Vijay Leo dialogue speech"]),
        "super": ("Bloody Sweet! I am waiting!", ["Vijay Leo Bloody Sweet dialogue"]),
        "win": ("En nenjil kudiyirukkum", ["Vijay Leo thozhargale speech"]),
        "bark1": ("What bro? It's very wrong bro!", ["Vijay Tamil interview what bro"]),
        "bark2": ("Bloody Sweet!", ["Vijay Leo Bloody Sweet"]),
    },
    "didi": {
        "intro": ("Unmaiyana makkal iyakkam", ["Jayalalithaa Tamil speech makkal iyakkam"]),
        "special1": ("Naan Ninaithal", ["Jayalalithaa Tamil speech Naan Ninaithal"]),
        "special2": ("Naan irukkindra varai, enakkup pinnalum", ["Jayalalithaa Tamil win speech"]),
        "super": ("Naan Ninaithal...!", ["Jayalalithaa Naan Ninaithal Tamil speech"]),
        "win": ("Naan irukkindra varai, enakkup pinnalum", ["Jayalalithaa Amma speech"],
        ),
        "bark1": ("Unmaiyana makkal iyakkam", ["Jayalalithaa Tamil public address"]),
        "bark2": ("Naan irukkindra varai", ["Jayalalithaa Tamil crowd speech"]),
    },
    "trump": {
        "intro": ("Pushpa Pushparaj... Thaggedhe Le!", ["Allu Arjun Pushpa Thaggedhe Le Tamil dubbed"]),
        "special1": ("Pushpa ante flower-a? Fireuu!", ["Allu Arjun Pushpa flower fire dialogue Tamil"]),
        "special2": ("Pushpa ante flower-a? Fireuu!", ["Allu Arjun Pushpa interval dialogue"]),
        "super": ("Pushpa ante flower anukunnava? FIRE!", ["Allu Arjun Pushpa pre interval fire dialogue"]),
        "win": ("Pushpa ante flower-a? Fireuu!", ["Allu Arjun Pushpa Flower Fire Tamil"]),
        "bark1": ("Thaggedhe Le!", ["Allu Arjun Pushpa Thaggedhe Le"]),
        "bark2": ("Pushpa ante flower-a?", ["Allu Arjun Pushpa flower dialogue"]),
    },
    "yogi": {
        "intro": ("Mukhyamantri kaserayil aakam", ["Pinarayi Vijayan Malayalam speech"]),
        "special1": ("Kadakku Purathu", ["Pinarayi Vijayan Kadakku Purathu speech"]),
        "special2": ("Entho undakki kalayam ennanaanu vicharikunnathu", ["Pinarayi Vijayan Malayalam public speech"]),
        "super": ("Kadakku Purathu!", ["Pinarayi Vijayan famous Kadakku Purathu address"]),
        "win": ("Entho undakki kalayam ennanaanu vicharikunnathu", ["Pinarayi Vijayan Malayalam statement"]),
        "bark1": ("Mukhyamantri kaserayil aakam", ["Pinarayi Vijayan Malayalam address"]),
        "bark2": ("Kadakku Purathu", ["Pinarayi Vijayan Kadakku Purathu"]),
    },
    "nitin": {
        "intro": ("One thing I'd like to tell you - my birthday", ["DK Shivakumar birthday speech English"]),
        "special1": ("Kanakapura Bande", ["DK Shivakumar Kanakapura Bande speech"]),
        "special2": ("By profession I'm a businessman", ["DK Shivakumar businessman interview"]),
        "super": ("Kanakapura Bande!", ["DK Shivakumar Kanakapura Bande original"]),
        "win": ("By profession I'm a businessman", ["DK Shivakumar press meet businessman"]),
        "bark1": ("One thing I'd like to tell you", ["DK Shivakumar birthday press statement"]),
        "bark2": ("Operation Success! 5 Guarantees", ["DK Shivakumar guarantee speech"]),
    },
    "ravi": {
        "intro": ("Naaku konchem thikka undhi, kaani daniko lekka undhi", ["Pawan Kalyan Telugu thikka undhi speech"]),
        "special1": ("Seize the Ship", ["Pawan Kalyan Seize the Ship speech"]),
        "special2": ("Janamlo unta! Janam la unta!", ["Pawan Kalyan Telugu Janamlo unta speech"]),
        "super": ("Seize the Ship!", ["Pawan Kalyan OG seize the ship original"]),
        "win": ("Janamlo unta! Janam la unta!", ["Pawan Kalyan Telugu public speech"]),
        "bark1": ("Naaku konchem thikka undhi", ["Pawan Kalyan Telugu campaign speech"]),
        "bark2": ("Janamlo unta", ["Pawan Kalyan Janamlo unta"]),
    },
    "lalu": {
        "intro": ("Moondru yaanaigal uyirizhundhirukkindranar", ["Seeman Tamil three elephants speech"]),
        "special1": ("Oru thadava saappittu 27,000 vidhaigal vidhaikkudhu", ["Seeman Aamai Kari 27000 varieties speech"]),
        "special2": ("1500 yaanai irundhuchu... ippa 650 thaan!", ["Seeman Tamil elephant speech"]),
        "super": ("Aamai Kari 27,000 vidhaigal", ["Seeman Tamil Aamai Kari speech"]),
        "win": ("1500 yaanai irundhuchu", ["Seeman elephant Tamil speech"]),
        "bark1": ("Moondru yaanaigal uyirizhundhirukkindranar", ["Seeman Tamil elephant address"]),
        "bark2": ("Vaigai Express uruttu illa", ["Seeman Tamil Vaigai Express speech"]),
    },
    "mbapu": {
        "intro": ("Kadavul kitta undiyal vekkiringale - adhu Aathigam", ["Periyar Tamil Kadavul undiyal Aathigam"]),
        "special1": ("Vengayam Pagutharivu", ["Periyar rationalism Tamil onion speech"]),
        "special2": ("Nambamal poottu podringle - adhu thaan Naathigam", ["Periyar Tamil Nambamal Naathigam"]),
        "super": ("Pagutharivu Thee!", ["Periyar Tamil rationalist speech"]),
        "win": ("Nambamal poottu podringle", ["Periyar Nambamal Tamil speech"]),
        "bark1": ("Kadavul kitta undiyal", ["Periyar Kadavul kitta undiyal speech"]),
        "bark2": ("Suyamariyadhai", ["Periyar Tamil self respect speech"]),
    },
    "amit": {
        "intro": ("Adhukkellam bayappadathinga", ["Annamalai Tamil press meet speech"]),
        "special1": ("Naan solren kekuringala?", ["Annamalai Tamil Naan solren press meet"]),
        "special2": ("Ellathaiyum paathutten! Ellathaiyum paathachu!", ["Annamalai Tamil press meet ellathaiyum"]),
        "super": ("En Mann En Makkal - Checkmate!", ["Annamalai Tamil press meet checkmate"]),
        "win": ("Ellathaiyum paathutten", ["Annamalai Tamil press conference"]),
        "bark1": ("Adhukkellam bayappadathinga", ["Annamalai Tamil speech bayappadathinga"]),
        "bark2": ("Secret files press meet", ["Annamalai press meet secret file"]),
    },
    "dhruv": {
        "intro": ("Hello everyone, naan Madan Gowri!", ["Madan Gowri hello everyone intro"]),
        "special1": ("Hello my dear MG Squad!", ["Madan Gowri MG Squad intro"]),
        "special2": ("Indha video motivational video-va illa inspirational-a", ["Madan Gowri motivational inspirational speech"]),
        "super": ("Hello everyone, naan Madan Gowri!", ["Madan Gowri hello everyone original"]),
        "win": ("Indha video motivational video-va illa inspirational-a", ["Madan Gowri Tamil video motivational"]),
        "bark1": ("Hello Squad Bro", ["Madan Gowri Squad Bro Tamil"]),
        "bark2": ("Wikipedia tab", ["Madan Gowri Wikipedia Tamil"]),
    },
    "nirmala": {
        "intro": ("Waise parivar se aati hoon jahan onion rakhte hi nahi", ["Nirmala Sitharaman onion speech"]),
        "special1": ("Popcorn-ukkum 18% GST", ["Nirmala Sitharaman popcorn GST 18 percent"]),
        "special2": ("Social media: popcorn ke upar bhi daal rahe hain tax", ["Nirmala Sitharaman popcorn tax speech"]),
        "super": ("Cream Bun-ukkum GST!", ["Nirmala Sitharaman GST speech"]),
        "win": ("Social media: popcorn ke upar bhi daal rahe hain tax", ["Nirmala Sitharaman social media GST"]),
        "bark1": ("Waise parivar se aati hoon", ["Nirmala Sitharaman onion family speech"]),
        "bark2": ("Popcorn ke upar tax", ["Nirmala Sitharaman popcorn tax"]),
    },
    "rangaraj": {
        "intro": ("Edhirkatchi thalaivarum pradhanarum pesittu iruppanga", ["Rangaraj Pandey debate intro Tamil"]),
        "special1": ("Kelvikku enna bathil?", ["Rangaraj Pandey Kelvikku enna bathil"]),
        "special2": ("Irandaavadhu point vandhu - Bharat Pradhanam", ["Rangaraj Pandey prime time point debate"]),
        "super": ("Dhairiyam purusha latchanam", ["Rangaraj Pandey dhairiyam purusha latchanam"]),
        "win": ("Irandaavadhu point vandhu", ["Rangaraj Pandey debate point"]),
        "bark1": ("Point-ku vaanga", ["Rangaraj Pandey Tamil point debate"]),
        "bark2": ("Mic mute pannidatta?", ["Rangaraj Pandey mic mute debate"]),
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Curate, cut, and verify real fighter voice lines")
    parser.add_argument("--cache-dir", default=".audio_cache", help="Transcript and source cache directory")
    parser.add_argument("--fighters", default="", help="Comma-separated fighter IDs (default: all)")
    parser.add_argument("--whisper-model", default="small", help="faster-whisper model name")
    parser.add_argument("--source-mode", choices=("local", "fetch"), default="local", help="Candidate discovery mode")
    parser.add_argument("--dry-run", action="store_true", help="Inspect candidates without transcribing or writing")
    parser.add_argument("--fetch-limit", type=int, default=5, help="Maximum fetched candidates per fighter")
    return parser.parse_args()


def normalized_words(text: str) -> List[str]:
    return re.findall(r"[^\W\d_]+(?:['-][^\W\d_]+)*", text.lower(), flags=re.UNICODE)


def match_score(expected: str, actual: str) -> float:
    expected_words = normalized_words(expected)
    actual_words = normalized_words(actual)
    if not expected_words:
        return 1.0 if not actual_words else 0.0
    if not actual_words:
        return 0.0
    return round(SequenceMatcher(None, " ".join(expected_words), " ".join(actual_words)).ratio(), 3)


def audio_path(source: str) -> Optional[Path]:
    if not source:
        return None
    relative = source.lstrip("/\\")
    path = PUBLIC_DIR / relative
    return path if path.is_file() else None


def duration_limit(line_id: str) -> Optional[float]:
    if line_id.startswith("bark"):
        return LIMITS["bark"]
    if line_id.startswith("special"):
        return LIMITS["special"]
    if line_id in LIMITS:
        return LIMITS[line_id]
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


def load_model(model_name: str):
    from faster_whisper import WhisperModel
    cache_key = model_name
    if not hasattr(load_model, "_cache"):
        load_model._cache = {}
    if cache_key not in load_model._cache:
        load_model._cache[cache_key] = WhisperModel(model_name, device="auto", compute_type="auto")
    return load_model._cache[cache_key]


def transcribe_full(path: Path, model_name: str, cache_dir: Path) -> Dict:
    digest = hashlib.sha256(f"{path.resolve()}|{model_name}|full-v2".encode("utf-8")).hexdigest()[:20]
    cache_file = cache_dir / "transcripts" / f"{digest}.json"
    if cache_file.is_file():
        return json.loads(cache_file.read_text(encoding="utf-8"))

    try:
        model = load_model(model_name)
    except Exception as exc:
        return {"text": "", "words": [], "language": "", "languageProbability": 0.0,
                "error": f"faster-whisper unavailable: {exc}"}

    try:
        segments, info = model.transcribe(
            str(path),
            word_timestamps=True,
            vad_filter=True,
            beam_size=5,
        )
        segment_list = list(segments)
    except Exception as exc:
        return {"text": "", "words": [], "language": "", "languageProbability": 0.0,
                "error": f"transcription failed: {exc}"}

    words = []
    for segment in segment_list:
        for word in getattr(segment, "words", []) or []:
            token = word.word.strip()
            if token:
                words.append({"word": token, "start": float(word.start), "end": float(word.end)})
    result = {
        "text": " ".join(segment.text.strip() for segment in segment_list).strip(),
        "words": words,
        "language": getattr(info, "language", "") or "",
        "languageProbability": round(float(getattr(info, "language_probability", 0.0)), 4),
    }
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    cache_file.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


def sliding_window_match(target: str, words: List[Dict]) -> Optional[Tuple[float, float, float, str]]:
    target_words = normalized_words(target)
    if not target_words or not words:
        return None
    target_joined = " ".join(target_words)
    window_count = len(target_words)
    best = None
    for span in range(max(1, window_count - 4), window_count + 5):
        for index in range(0, max(1, len(words) - span + 1)):
            window = words[index:index + span]
            candidate = " ".join(normalized_words(" ".join(w["word"] for w in window)))
            score = match_score(target_joined, candidate)
            if best is None or score > best[0]:
                best = (score, float(window[0]["start"]), float(window[-1]["end"]), candidate)
    return best


def cut_exact(source: Path, destination: Path, start: float, end: float, maximum: float) -> bool:
    destination.parent.mkdir(parents=True, exist_ok=True)
    duration = max(0.08, min(maximum, end - start))
    start = max(0.0, start - 0.06)
    end = start + duration + 0.06
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    args = [
        ffmpeg, "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(source),
        "-ss", f"{start:.3f}", "-to", f"{end:.3f}",
        "-af", "afade=t=in:d=0.025,afade=t=out:st=%.3f:d=0.025,loudnorm=I=-14:TP=-1.2:LRA=9" % max(0.0, duration - 0.025),
        "-ar", "44100", "-ac", "2", str(destination),
    ]
    try:
        return subprocess.run(args, capture_output=True, timeout=120).returncode == 0
    except Exception:
        return False


def get_reference_embedding(reference: Path) -> Optional[object]:
    try:
        import numpy as np
        from resemblyzer import VoiceEncoder, preprocess_wav
        wav = preprocess_wav(str(reference))
        embedding = VoiceEncoder().embed_utterance(wav)
        return np.asarray(embedding)
    except Exception:
        return None


def speaker_score(reference_embedding: Optional[object], candidate: Path) -> float:
    if reference_embedding is None:
        return 0.0
    try:
        import numpy as np
        from resemblyzer import VoiceEncoder, preprocess_wav
        wav = preprocess_wav(str(candidate))
        embedding = np.asarray(VoiceEncoder().embed_utterance(wav))
        score = float(np.dot(reference_embedding, embedding) /
                      (np.linalg.norm(reference_embedding) * np.linalg.norm(embedding)))
        return round(max(0.0, min(1.0, score)), 3)
    except Exception:
        return 0.0


def local_candidates(fighter: str, cache_dir: Path) -> List[Path]:
    candidates = []
    roots = [
        PUBLIC_DIR / "assets" / "memes",
        PUBLIC_DIR / "assets",
        cache_dir / "candidates" / fighter,
        cache_dir / "clips" / fighter,
    ]
    for root in roots:
        if not root.is_dir():
            continue
        patterns = (
            f"{fighter}_*.mp3",
            f"{fighter}-*.mp3",
            f"{fighter}*.mp3",
            f"*{fighter}*.wav",
            f"*{fighter}*.m4a",
        )
        for pattern in patterns:
            for path in sorted(root.glob(pattern)):
                if path.is_file() and path not in candidates:
                    candidates.append(path)
    return candidates


def fetch_candidates(fighter: str, cache_dir: Path, queries: List[str], limit: int) -> List[Path]:
    if yt_dlp is None:
        return []
    candidates_dir = cache_dir / "candidates" / fighter
    candidates_dir.mkdir(parents=True, exist_ok=True)
    candidates = []
    query = " ".join(dict.fromkeys(queries[:3]))
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": False,
        "format": "bestaudio/best",
        "outtmpl": str(candidates_dir / "%(id)s.%(ext)s"),
        "noplaylist": True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            results = ydl.extract_info(f"ytsearch{limit}:{query}", download=False)
            entries = results.get("entries", []) if isinstance(results, dict) else []
            for entry in entries:
                if not isinstance(entry, dict) or not entry.get("webpage_url"):
                    continue
                info = ydl.extract_info(entry["webpage_url"], download=True)
                requested = info.get("requested_downloads", []) if isinstance(info, dict) else []
                candidate_paths = [
                    Path(download["filepath"]) for download in requested
                    if isinstance(download, dict) and download.get("filepath")
                ]
                if not candidate_paths and isinstance(info, dict) and info.get("filepath"):
                    candidate_paths = [Path(info["filepath"])]
                for path in candidate_paths:
                    if path.is_file() and path not in candidates:
                        candidates.append(path)
    except Exception as exc:
        print(f"fetch candidate discovery failed for {fighter}: {exc}", file=sys.stderr)
    return candidates[:limit]


def find_reference(fighter: str, data: Dict) -> Optional[Path]:
    entries = data.get(fighter, {})
    if not isinstance(entries, dict):
        return None
    for line_id in ("intro", "special1", "special2", "bark1", "bark2", "win", "super"):
        entry = entries.get(line_id)
        if isinstance(entry, dict):
            path = audio_path(entry.get("audio", ""))
            if path is not None:
                return path
    return None


def process_voice_lines(
    data: Dict,
    fighter_ids: Iterable[str],
    cache_dir: Path,
    model_name: str,
    source_mode: str,
    dry_run: bool,
    fetch_limit: int,
) -> tuple[Dict, List[Dict]]:
    selected = set(fighter_ids)
    updated = json.loads(json.dumps(data))
    rows = []

    for fighter, lines in updated.items():
        if selected and fighter not in selected:
            continue
        targets = ICONIC_DIALOGUE_TARGETS.get(fighter, {})
        reference = find_reference(fighter, data)
        reference_embedding = None if dry_run or reference is None else get_reference_embedding(reference)
        queries = []
        for target in targets.values():
            if isinstance(target, tuple):
                queries.extend(target[1])

        candidates = []
        if dry_run or source_mode == "local":
            candidates = local_candidates(fighter, cache_dir)
        if source_mode == "fetch":
            candidates = fetch_candidates(fighter, cache_dir, queries, fetch_limit)

        for line_id, entry in lines.items():
            if not isinstance(entry, dict):
                continue
            target_data = targets.get(line_id)
            target_phrase = target_data[0] if isinstance(target_data, tuple) else entry.get("text", "")
            if line_id in ("bark1", "bark2", "special1", "special2") and not target_phrase:
                continue
            entry["iconicTarget"] = target_phrase
            entry["searchQueries"] = target_data[1] if isinstance(target_data, tuple) else []
            entry["sourceMode"] = source_mode
            entry.setdefault("durationMs", duration_limit(line_id) * 1000 if duration_limit(line_id) else 3000)
            entry["approved"] = False
            entry["needsReview"] = True
            entry["matchScore"] = 0.0
            entry["speakerScore"] = 0.0

            fallback_source = entry.get("audio", "")
            fallback_path = audio_path(fallback_source)
            if dry_run:
                rows.append({
                    "fighter": fighter,
                    "line": line_id,
                    "source": str(candidates[0]) if candidates else fallback_source,
                    "match": 0.0,
                    "speaker": 0.0,
                    "missing": not candidates,
                    "approved": False,
                    "needsReview": True,
                    "fallback": fallback_source,
                    "target": target_phrase,
                })
                continue

            if not candidates:
                entry["needsReview"] = True
                entry["approved"] = False
                entry["fallbackSource"] = fallback_source
                rows.append({
                    "fighter": fighter,
                    "line": line_id,
                    "source": fallback_source,
                    "match": 0.0,
                    "speaker": 0.0,
                    "missing": fallback_path is None,
                    "approved": False,
                    "needsReview": True,
                    "fallback": fallback_source,
                    "target": target_phrase,
                })
                continue

            best = None
            for candidate in candidates:
                full = transcribe_full(candidate, model_name, cache_dir)
                if "error" in full:
                    entry["transcriptError"] = full["error"]
                    continue
                match = sliding_window_match(target_phrase, full.get("words", []))
                if match is None:
                    continue
                text_score, start, end, candidate_text = match
                if text_score < 0.75:
                    continue

                exact_dir = cache_dir / "exact-cuts" / fighter
                exact_dir.mkdir(parents=True, exist_ok=True)
                exact = exact_dir / f"{line_id}-{hashlib.sha256(str(candidate).encode()).hexdigest()[:10]}-exact.mp3"
                maximum = duration_limit(line_id) or 3.5
                if not cut_exact(candidate, exact, start, end, maximum):
                    continue

                retranscribe = transcribe_full(exact, model_name, cache_dir)
                exact_score = match_score(target_phrase, retranscribe.get("text", ""))
                sp_score = speaker_score(reference_embedding, exact)
                approved = exact_score >= 0.75 and sp_score >= 0.70
                record = (exact_score, sp_score, exact, start, end, retranscribe)
                if best is None or (exact_score + sp_score) > (best[0] + best[1]):
                    best = record
                if approved:
                    break

            if best is None:
                entry["needsReview"] = True
                entry["approved"] = False
                entry["fallbackSource"] = fallback_source
                rows.append({
                    "fighter": fighter,
                    "line": line_id,
                    "source": fallback_source,
                    "match": 0.0,
                    "speaker": 0.0,
                    "missing": fallback_path is None,
                    "approved": False,
                    "needsReview": True,
                    "fallback": fallback_source,
                    "target": target_phrase,
                })
                continue

            exact_score, sp_score, exact, start, end, retranscribe = best
            entry["matchScore"] = round(exact_score, 3)
            entry["speakerScore"] = round(sp_score, 3)
            entry["whisperText"] = retranscribe.get("text", "")
            entry["cutStart"] = round(start, 3)
            entry["cutEnd"] = round(end, 3)
            approved = exact_score >= 0.75 and sp_score >= 0.70
            entry["approved"] = approved
            entry["needsReview"] = not approved
            entry["fallbackSource"] = fallback_source

            if approved:
                voice_dir = PUBLIC_DIR / "assets" / "voice"
                destination = voice_dir / fighter / f"{line_id}.mp3"
                destination.parent.mkdir(parents=True, exist_ok=True)
                exact_duration = ffprobe_duration(exact)
                entry["durationMs"] = round((exact_duration or duration_limit(line_id) or 3.0) * 1000)
                if str(exact).replace("\\", "/") != str(destination).replace("\\", "/"):
                    import shutil
                    shutil.copy2(exact, destination)
                entry["audio"] = f"/assets/voice/{fighter}/{line_id}.mp3"
                entry["source"] = str(exact)
            else:
                entry["audio"] = fallback_source
                entry["source"] = fallback_source

            rows.append({
                "fighter": fighter,
                "line": line_id,
                "source": entry["audio"],
                "match": exact_score,
                "speaker": sp_score,
                "missing": fallback_path is None,
                "approved": approved,
                "needsReview": not approved,
                "fallback": fallback_source,
                "target": target_phrase,
            })

    return updated, rows


def print_summary(rows: List[Dict]) -> None:
    print(f"{'FIGHTER':12} {'LINE':12} {'STATUS':18} {'MATCH':>6} {'SPEAKER':>8}")
    print("-" * 66)
    review = 0
    for row in rows:
        statuses = []
        if row["missing"]:
            statuses.append("missing")
        if row["match"] < 0.75:
            statuses.append("match<0.75")
        if row["speaker"] < 0.70:
            statuses.append("speaker<0.70")
        if row.get("approved"):
            status = "approved"
        else:
            status = ", ".join(statuses) or "needsReview"
        print(f"{row['fighter']:12} {row['line']:12} {status:18} {row['match']:6.3f} {row['speaker']:8.3f}")
        if not row.get("approved"):
            review += 1
    print(f"\n{review} line(s) need review")


def main() -> int:
    args = parse_args()
    cache_dir = (ROOT / args.cache_dir).resolve() if not os.path.isabs(args.cache_dir) else Path(args.cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    fighter_ids = [value.strip() for value in args.fighters.split(",") if value.strip()]

    if not VOICE_JSON.is_file():
        print(f"Missing voice-lines file: {VOICE_JSON}", file=sys.stderr)
        return 1
    data = json.loads(VOICE_JSON.read_text(encoding="utf-8"))
    updated, rows = process_voice_lines(
        data,
        fighter_ids,
        cache_dir,
        args.whisper_model,
        args.source_mode,
        args.dry_run,
        args.fetch_limit,
    )

    if not args.dry_run:
        tmp = VOICE_JSON.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(updated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        os.replace(tmp, VOICE_JSON)
    print_summary(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
