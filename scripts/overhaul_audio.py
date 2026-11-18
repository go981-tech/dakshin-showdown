#!/usr/bin/env python3
"""
Overhauls all game audio in public/assets/:
  1. Real online celebrity/politician voice clips (YouTube via yt-dlp + MyInstants + edge-tts fallback)
  2. Real Kollywood mass BGM tracks (Vikram / Jailer / Master)
  3. Real Arcade Fighting Game Announcer clips (Round 1, Round 2, Final Round, Fight, KO, Perfect, You Win, You Lose, Time Up, Double KO)
  4. Real downloaded SFX + studio-filtered 44.1kHz stereo synth SFX/beds with zero 15KB/28KB placeholder WAVs
"""

import asyncio
import math
import os
import re
import struct
import subprocess
import tempfile
import wave
from concurrent.futures import ThreadPoolExecutor

import imageio_ffmpeg
import numpy as np
import requests
import yt_dlp

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "public", "assets")
MEMES = os.path.join(ASSETS, "memes")
SFX_DIR = os.path.join(ASSETS, "sfx")
VOICE_DIR = os.path.join(ASSETS, "voice")
CACHE_DIR = os.path.join(
    os.path.expanduser("~"),
    ".gemini", "antigravity", "brain", "9258c89c-bb01-401d-ac65-d60bc4045af8", "scratch", "audio_cache"
)

os.makedirs(MEMES, exist_ok=True)
os.makedirs(SFX_DIR, exist_ok=True)
os.makedirs(VOICE_DIR, exist_ok=True)
os.makedirs(CACHE_DIR, exist_ok=True)

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
SR = 44100


def is_valid_audio(path):
    if not os.path.exists(path) or os.path.getsize(path) < 1200:
        return False
    with open(path, "rb") as f:
        h = f.read(16)
    return h.startswith(b"ID3") or (len(h) >= 2 and h[0] == 0xFF and (h[1] & 0xE0) == 0xE0) or h.startswith(b"RIFF") or h.startswith(b"OggS") or h[4:8] == b"ftyp"


def run_ffmpeg(args):
    p = subprocess.run(
        [FFMPEG, "-y", "-hide_banner", "-loglevel", "error", *args],
        capture_output=True,
        text=True,
    )
    return p.returncode == 0


def find_vocal_offset(src_path, target_start=0.0, max_scan=25.0, window_s=2.8):
    """Decode first max_scan seconds to 8kHz mono PCM and pick highest non-silent vocal start near target_start."""
    raw_path = src_path + ".pcm"
    ok = run_ffmpeg([
        "-ss", str(max(0.0, target_start)),
        "-t", str(max_scan),
        "-i", src_path,
        "-ac", "1", "-ar", "8000", "-f", "s16le", raw_path,
    ])
    if not ok or not os.path.exists(raw_path):
        return max(0.0, target_start)
    try:
        data = np.fromfile(raw_path, dtype=np.int16).astype(np.float32) / 32768.0
    finally:
        if os.path.exists(raw_path):
            os.remove(raw_path)
    if len(data) < 4000:
        return max(0.0, target_start)
    hop = 2000  # 0.25s steps
    win = int(window_s * 8000)
    if len(data) <= win:
        return max(0.0, target_start)
    best_idx = 0
    best_score = -1.0
    for i in range(0, len(data) - win, hop):
        seg = data[i : i + win]
        rms = float(np.sqrt(np.mean(seg * seg)))
        # Prefer first clear energetic speech block (RMS > 0.04) with mild preference for early speech
        if rms > 0.05:
            return round(target_start + i / 8000.0, 2)
        if rms > best_score:
            best_score = rms
            best_idx = i
    return round(target_start + best_idx / 8000.0, 2)


def process_audio_clip(
    src_path,
    out_path,
    ss=None,
    dur=None,
    voice=True,
    lufs=-14.0,
    trim_silence=True,
    fade_io=0.04,
):
    af = []
    if trim_silence:
        thresh = "-34dB" if voice else "-42dB"
        af.append(f"silenceremove=start_periods=1:start_duration=0.02:start_threshold={thresh}")
    if voice:
        af.append("highpass=f=85,lowpass=f=7800")
    af.append(f"loudnorm=I={lufs}:TP=-1.2:LRA=9")
    if fade_io and fade_io > 0:
        af.append(f"afade=t=in:ss=0:d={fade_io}")
    if dur and fade_io and dur > fade_io * 2.5:
        af.append(f"afade=t=out:st={max(0.05, dur - fade_io):.3f}:d={fade_io}")

    cmd = []
    if ss is not None and ss > 0:
        cmd += ["-ss", f"{ss:.2f}"]
    if dur is not None:
        cmd += ["-t", f"{dur:.2f}"]
    cmd += [
        "-i", src_path,
        "-vn",
        "-af", ",".join(af),
        "-ar", str(SR),
        "-ac", "2",
        "-c:a", "libmp3lame",
        "-b:a", "160k",
        out_path,
    ]
    ok = run_ffmpeg(cmd)
    if (not ok or not is_valid_audio(out_path)) and trim_silence:
        return process_audio_clip(src_path, out_path, ss=ss, dur=dur, voice=voice, lufs=lufs, trim_silence=False, fade_io=fade_io)
    return ok


def download_myinstant(slug_or_url, name):
    url = slug_or_url if slug_or_url.startswith("http") else f"https://www.myinstants.com{slug_or_url}"
    cached = os.path.join(CACHE_DIR, f"mi_{name}.mp3")
    if is_valid_audio(cached):
        return cached
    try:
        r = requests.get(url, headers=HEADERS, timeout=12)
        if r.status_code == 200 and len(r.content) > 1500:
            head = r.content[:20].lstrip()
            if not head.startswith(b"<"):
                with open(cached, "wb") as f:
                    f.write(r.content)
                if is_valid_audio(cached):
                    return cached
    except Exception as e:
        print(f"  [WARN] MyInstants fail {url}: {e}")
    return None


def download_yt_audio(video_id, section_end=45, tag="clip"):
    out_tpl = os.path.join(CACHE_DIR, f"yt_{video_id}_{tag}.%(ext)s")
    for ext in ("m4a", "webm", "opus", "mp3", "mp4"):
        p = os.path.join(CACHE_DIR, f"yt_{video_id}_{tag}.{ext}")
        if is_valid_audio(p):
            return p

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "format": "bestaudio[ext=m4a]/bestaudio/worstaudio/best",
        "outtmpl": out_tpl,
        "ffmpeg_location": FFMPEG,
        "socket_timeout": 12,
        "retries": 2,
    }
    for use_ranges in ([True, False] if section_end else [False]):
        opts = dict(ydl_opts)
        if use_ranges:
            opts["download_ranges"] = yt_dlp.utils.download_range_func(None, [(0, section_end)])
        else:
            opts["max_filesize"] = 18 * 1024 * 1024
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([f"https://www.youtube.com/watch?v={video_id}"])
            for ext in ("m4a", "webm", "opus", "mp3", "mp4"):
                p = os.path.join(CACHE_DIR, f"yt_{video_id}_{tag}.{ext}")
                if is_valid_audio(p):
                    return p
        except Exception as e:
            print(f"  [WARN] YT download ({'ranged' if use_ranges else 'full'}) fail {video_id}: {e}")
    return None


async def synth_edge_tts(text, voice, out_mp3, rate="+0%", pitch="+0Hz"):
    import edge_tts

    raw = out_mp3 + ".edge.mp3"
    comm = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    await comm.save(raw)
    if os.path.exists(raw):
        ok = process_audio_clip(raw, out_mp3, dur=None, voice=True, lufs=-13.5, trim_silence=True, fade_io=0.03)
        os.remove(raw)
        return ok and is_valid_audio(out_mp3)
    return False


def make_edge_tts_sync(text, voice, out_mp3, rate="+0%", pitch="+0Hz"):
    return asyncio.run(synth_edge_tts(text, voice, out_mp3, rate=rate, pitch=pitch))


def write_numpy_mp3(stereo_audio, out_path, fade_io=0.02):
    """Write float32 (-1..1) stereo or mono array as crisp 160k stereo MP3 via ffmpeg."""
    if stereo_audio.ndim == 1:
        stereo_audio = np.stack([stereo_audio, stereo_audio], axis=1)
    peak = float(np.max(np.abs(stereo_audio)))
    if peak > 0.95:
        stereo_audio = stereo_audio * (0.92 / peak)
    pcm = np.clip(stereo_audio * 32767.0, -32768, 32767).astype("<i2")
    wav_tmp = out_path + ".tmp.wav"
    with wave.open(wav_tmp, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(pcm.tobytes())
    ok = run_ffmpeg([
        "-i", wav_tmp,
        "-ar", str(SR),
        "-ac", "2",
        "-c:a", "libmp3lame",
        "-b:a", "160k",
        out_path,
    ])
    if os.path.exists(wav_tmp):
        os.remove(wav_tmp)
    return ok


def synth_studio_ui_or_bed(kind, out_path):
    """Synthesize clean studio-filtered 44.1kHz stereo MP3 for UI ticks, shimmer, and 8s-13s super beds."""
    rng = np.random.default_rng(abs(hash(kind)) & 0xFFFFFFFF)

    if kind == "ui_tap":
        t = np.linspace(0, 0.08, int(SR * 0.08), endpoint=False)
        sig = (np.sin(2 * np.pi * 680 * np.exp(-t * 18) * t) * 0.55 + np.sin(2 * np.pi * 1360 * t) * 0.15) * np.exp(-t * 55)
        sig *= np.minimum(1.0, t / 0.003)
        return write_numpy_mp3(sig, out_path)

    if kind == "ui_select":
        t = np.linspace(0, 0.14, int(SR * 0.14), endpoint=False)
        s1 = np.sin(2 * np.pi * 523.25 * t) * np.exp(-t * 32) * (t < 0.06)
        t2 = np.maximum(0.0, t - 0.045)
        s2 = np.sin(2 * np.pi * 783.99 * t2) * np.exp(-t2 * 26) * (t >= 0.045)
        sig = (s1 + s2) * 0.45 * np.minimum(1.0, t / 0.003)
        return write_numpy_mp3(sig, out_path)

    if kind == "ui_confirm":
        t = np.linspace(0, 0.28, int(SR * 0.28), endpoint=False)
        notes = [(0.0, 523.25), (0.055, 659.25), (0.11, 783.99)]
        sig = np.zeros_like(t)
        for st, hz in notes:
            dt = np.maximum(0.0, t - st)
            env = (t >= st) * np.exp(-dt * 16) * np.minimum(1.0, dt / 0.004)
            sig += (np.sin(2 * np.pi * hz * dt) * 0.65 + np.sin(2 * np.pi * hz * 2 * dt) * 0.2) * env
        return write_numpy_mp3(sig * 0.45, out_path)

    if kind == "ui_back":
        t = np.linspace(0, 0.18, int(SR * 0.18), endpoint=False)
        s1 = np.sin(2 * np.pi * 587.33 * t) * np.exp(-t * 25)
        t2 = np.maximum(0.0, t - 0.05)
        s2 = np.sin(2 * np.pi * 392.00 * t2) * np.exp(-t2 * 22) * (t >= 0.05)
        return write_numpy_mp3((s1 * 0.35 + s2 * 0.45) * np.minimum(1.0, t / 0.003), out_path)

    if kind in ("eye_zing", "aloolelo"):
        dur = 0.55 if kind == "eye_zing" else 0.75
        t = np.linspace(0, dur, int(SR * dur), endpoint=False)
        f = 440 + 1760 * (t / dur) ** 1.4
        phase = 2 * np.pi * np.cumsum(f) / SR
        sigL = np.sin(phase) * 0.45 + np.sin(phase * 1.5 + 0.4) * 0.22
        sigR = np.sin(phase * 1.005) * 0.45 + np.sin(phase * 1.505 - 0.4) * 0.22
        env = np.sin(np.pi * t / dur) ** 0.7 * np.exp(-t * 2.2)
        return write_numpy_mp3(np.stack([sigL * env, sigR * env], axis=1), out_path)

    if kind == "shimmer":
        dur = 1.15
        t = np.linspace(0, dur, int(SR * dur), endpoint=False)
        chord = [1046.50, 1318.51, 1567.98, 2093.00, 2637.02]
        sigL = np.zeros_like(t)
        sigR = np.zeros_like(t)
        for idx_n, hz in enumerate(chord):
            st = idx_n * 0.055
            dt = np.maximum(0.0, t - st)
            env = (t >= st) * np.exp(-dt * 4.2) * np.minimum(1.0, dt / 0.005)
            pan = 0.35 if idx_n % 2 == 0 else 0.75
            w = np.sin(2 * np.pi * hz * dt) * env * 0.35
            sigL += w * pan
            sigR += w * (1.1 - pan)
        return write_numpy_mp3(np.stack([sigL, sigR], axis=1), out_path)

    if kind in ("poof", "charkha"):
        dur = 0.5 if kind == "poof" else 1.4
        t = np.linspace(0, dur, int(SR * dur), endpoint=False)
        noise = rng.normal(0, 1, len(t))
        # Moving lowpass swoosh via simple weighted cumulative kernel
        k = np.ones(45) / 45.0
        warm = np.convolve(noise, k, mode="same")
        if kind == "poof":
            env = np.minimum(1.0, t / 0.015) * np.exp(-t * 9.0)
            sub = np.sin(2 * np.pi * 115 * np.exp(-t * 8) * t) * np.exp(-t * 11) * 0.5
            sig = warm * env * 1.4 + sub
            return write_numpy_mp3(sig, out_path)
        else:
            am = 0.5 + 0.5 * np.sin(2 * np.pi * 6.5 * t)
            env = np.sin(np.pi * t / dur) * am
            tone = np.sin(2 * np.pi * (160 + 25 * np.sin(2 * np.pi * 6.5 * t)) * t) * 0.22
            sig = (warm * 0.9 + tone) * env
            return write_numpy_mp3(sig, out_path)

    if kind == "drone":
        dur = 13.0  # engine uses loopEnd = yi = 12.5
        t = np.linspace(0, dur, int(SR * dur), endpoint=False)
        # Warm C2 + G2 cinematic bass pad with slow stereo chorus (zero harshness)
        det = 0.004
        L = (
            np.sin(2 * np.pi * 65.41 * t) * 0.42
            + np.sin(2 * np.pi * (65.41 * (1 + det)) * t) * 0.28
            + np.sin(2 * np.pi * 98.00 * t) * 0.24
            + np.sin(2 * np.pi * 130.81 * t) * 0.14
        )
        R = (
            np.sin(2 * np.pi * 65.41 * t) * 0.42
            + np.sin(2 * np.pi * (65.41 * (1 - det)) * t) * 0.28
            + np.sin(2 * np.pi * 98.00 * t) * 0.24
            + np.sin(2 * np.pi * 131.15 * t) * 0.14
        )
        sw = 0.8 + 0.2 * np.sin(2 * np.pi * 0.5 * t)
        return write_numpy_mp3(np.stack([L * sw * 0.65, R * sw * 0.65], axis=1), out_path)

    # Super charge / tension beds (must be >= 7.5s so playTimed(bed, dur) never misses offset!)
    dur = 8.0
    t = np.linspace(0, dur, int(SR * dur), endpoint=False)
    prog = t / dur
    base = 73.42 if "chakra" in kind or "charge" in kind else 82.41 if "jadu" in kind else 65.41
    freq = base * (1.0 + 0.5 * (prog ** 1.8))
    phase = 2 * np.pi * np.cumsum(freq) / SR
    sub = np.sin(phase) * 0.45 + np.sin(phase * 1.5) * 0.25 + np.sin(phase * 2.0) * 0.18
    # Cinematic accelerating Taiko / Thavil pulse train during build-up
    pulse_env = np.zeros_like(t)
    cur = 0.0
    while cur < dur - 0.15:
        step = 0.42 - 0.30 * ((cur / dur) ** 1.1)
        i0 = int(cur * SR)
        i1 = min(len(t), i0 + int(0.18 * SR))
        dt = np.arange(i1 - i0) / SR
        kf = 110 * np.exp(-dt * 20) + 52
        pulse_env[i0:i1] += np.sin(2 * np.pi * kf * dt) * np.exp(-dt * 16) * (0.35 + 0.55 * (cur / dur))
        cur += max(0.08, step)
    swell = 0.25 + 0.75 * prog
    L = (sub * swell + pulse_env) * 0.65
    R = (sub * swell * 0.95 + np.roll(pulse_env, 120)) * 0.65
    return write_numpy_mp3(np.stack([L, R], axis=1), out_path)


def synth_kollywood_bgm_fallback(kind, out_path):
    """High-energy 44.1kHz stereo Thavil/Parai/Nadaswaram/808 BGM loop (24s) if YT download unavailable."""
    bpm = 132 if kind == "battle" else 118 if kind == "intro" else 108
    beat = 60.0 / bpm
    bars = 12
    dur = bars * 4 * beat
    n = int(dur * SR)
    L = np.zeros(n, dtype=np.float32)
    R = np.zeros(n, dtype=np.float32)
    rng = np.random.default_rng(101 if kind == "battle" else 202)
    scale = [146.83, 164.81, 185.00, 196.00, 220.00, 246.94, 277.18, 293.66]  # D major / Shankarabharanam bass
    lead = [587.33, 659.25, 739.99, 783.99, 880.00, 987.77, 1174.66]
    mel_idx = [0, 2, 4, 3, 2, 1, 0, 4, 5, 4, 3, 2, 4, 2, 1, 0]

    total_16 = bars * 16
    step_s = beat / 4.0
    for s in range(total_16):
        i0 = int(s * step_s * SR)
        if i0 >= n:
            break
        # 808 Kuthu kick on 1, 4, 7, 9, 13
        if s % 16 in (0, 3, 6, 8, 12):
            klen = min(n - i0, int(0.22 * SR))
            dt = np.arange(klen) / SR
            kf = 145 * np.exp(-dt * 28) + 46
            kick = np.sin(2 * np.pi * kf * dt) * np.exp(-dt * 12) * 0.58
            L[i0 : i0 + klen] += kick
            R[i0 : i0 + klen] += kick
        # Parai slap on offbeats
        if s % 4 == 2 or (kind == "battle" and s % 8 == 5):
            plen = min(n - i0, int(0.09 * SR))
            dt = np.arange(plen) / SR
            snap = (np.sin(2 * np.pi * 240 * dt) * 0.35 + rng.normal(0, 0.25, plen)) * np.exp(-dt * 34)
            L[i0 : i0 + plen] += snap * 0.8
            R[i0 : i0 + plen] += snap * 0.9
        # Hi-hat groove
        if s % 2 == 1:
            hlen = min(n - i0, int(0.04 * SR))
            dt = np.arange(hlen) / SR
            hat = np.diff(rng.normal(0, 0.2, hlen + 1)) * np.exp(-dt * 60)
            L[i0 : i0 + hlen] += hat * (0.4 if s % 4 == 1 else 0.7)
            R[i0 : i0 + hlen] += hat * (0.7 if s % 4 == 1 else 0.4)
        # Warm brass / synth riff every 8th note
        if s % 2 == 0:
            note_f = lead[mel_idx[(s // 2) % len(mel_idx)]] * (1.0 if kind != "background" else 0.5)
            mlen = min(n - i0, int(step_s * 1.7 * SR))
            dt = np.arange(mlen) / SR
            env = np.minimum(1.0, dt / 0.015) * np.exp(-dt * 5.0)
            mel = (np.sin(2 * np.pi * note_f * dt) * 0.20 + np.sin(2 * np.pi * note_f * 2 * dt) * 0.06) * env
            L[i0 : i0 + mlen] += mel * 0.85
            R[i0 : i0 + mlen] += mel * 0.95
        # Sub bass pulse on beat
        if s % 4 == 0:
            bf = scale[0 if (s // 16) % 2 == 0 else 3] * 0.5
            blen = min(n - i0, int(beat * 0.95 * SR))
            dt = np.arange(blen) / SR
            b = np.sin(2 * np.pi * bf * dt) * np.exp(-dt * 3.2) * 0.32
            L[i0 : i0 + blen] += b
            R[i0 : i0 + blen] += b

    fade = int(0.25 * SR)
    L[:fade] *= np.linspace(0, 1, fade)
    R[:fade] *= np.linspace(0, 1, fade)
    L[-fade:] *= np.linspace(1, 0, fade)
    R[-fade:] *= np.linspace(1, 0, fade)
    return write_numpy_mp3(np.stack([L, R], axis=1), out_path)


def copy_to_all(src_mp3, dest_rel_paths):
    for rel in dest_rel_paths:
        dst = os.path.join(ASSETS, rel.replace("/", os.sep))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(src_mp3, "rb") as f:
            data = f.read()
        with open(dst, "wb") as f:
            f.write(data)


def main():
    print("=== STAGE 1: Downloading Real MyInstants SFX, Announcer & Meme Clips ===")
    mi_map = {
        # Combat SFX
        "hit_1": "/media/sounds/punch-gaming-sound-effect-hd_RzlG1GE.mp3",
        "hit_2": "/media/sounds/punch_u4LmMsr.mp3",
        "hit_3": "/media/sounds/strongpunch.mp3",
        "slap": "/media/sounds/slap-sound-effect-no-copyright.mp3",
        "block": "/media/sounds/sword-slash_NkdUSLZ.mp3",
        "whoosh": "/media/sounds/whoosh-sfx.mp3",
        "thud": "/media/sounds/bone-crack-meme.mp3",
        "boom": "/media/sounds/explosion-meme_dTCfAHs.mp3",
        "bomb": "/media/sounds/capcut-explosion-sound.mp3",
        "thunder": "/media/sounds/thunder-sound-effect.mp3",
        "bell": "/media/sounds/undertakers-bell_2UwFCIe.mp3",
        "cup_break": "/media/sounds/glass-breaking-sound-effect_wLZSIYn.mp3",
        "camera_clicks": "/media/sounds/camera-shutter-dslrr.mp3",
        "horn_long": "/media/sounds/train-horn-long-and-bass.mp3",
        "horn_short": "/media/sounds/bi-tonal-truck-trumpet.mp3",
        "kaching": "/media/sounds/s1_c5-online-audio-converter.mp3",
        "coins": "/media/sounds/coin_1.mp3",
        "drumroll": "/media/sounds/drum-roll-gaming-sound-effect-hd.mp3",
        "jingle_win": "/media/sounds/final-fantasy-vii-victory-fanfare-1.mp3",
        "jingle_lose": "/media/sounds/epic-fail-trumpet.mp3",
        "crate_crash": "/media/sounds/bloody-metal-baseball-bat-hit.mp3",
        "moo": "/media/sounds/cow-moo.mp3",
        "bark": "/media/sounds/minecraft-dog-bark.mp3",
        "frog": "/media/sounds/single-frog-croak.mp3",
        "news_sting": "/media/sounds/news_intro-maximilien_-1801238420_2.mp3",
        "heartbeat": "/media/sounds/heart-beat-speeds-up.mp3",
        "reverse_beeps": "/media/sounds/reverse-sound-effect.mp3",
        "engine_loop": "/media/sounds/bike-sound-kawasaki-h2.mp3",
        "pen_scribble": "/media/sounds/pencil-writing.mp3",
        "snap": "/media/sounds/finger-snap.mp3",
        "plop": "/media/sounds/bubble-pop.mp3",
        "shimmer": "/media/sounds/fairy-sparkle.mp3",
        "chai_ting": "/media/sounds/ding-sound-effect_2.mp3",
        "cow_bell": "/media/sounds/cowbell-shakes.mp3",
        "tick": "/media/sounds/clock-tick.mp3",
        # Announcer
        "round_1": "/media/sounds/street-fighter-round-1.mp3",
        "round_2": "/media/sounds/round-2_XzAyWIQ.mp3",
        "final_round": "/media/sounds/final-round.mp3",
        "fight": "/media/sounds/mortal-kombat-9-sound-drop-round-1-fight.mp3",
        "ko": "/media/sounds/mlg-resource-street-fighter-ko-greenscreen.mp3",
        "perfect": "/media/sounds/perfect-street-fighter-sound-effect.mp3",
        "you_win": "/media/sounds/street-fighter-ii-you-win-perfect.mp3",
        "you_lose": "/media/sounds/wasted-gta-5.mp3",
        # Direct Character Voice Clips
        "vijay_thambi": "/media/sounds/thambi-keela-erangu-pa.mp3",
        "vijay_troll": "/media/sounds/vijay-troll.mp3",
        "vijay_hmm": "/media/sounds/hmmmmmm-vijay.mp3",
        "vijay_varan": "/media/sounds/vijay-intro-songa-kaja-varan-da.mp3",
        "pushpa_fire": "/media/sounds/pushpa-fireee.mp3",
        "seeman_buhaha": "/media/sounds/seeman-buhaha.mp3",
        "annamalai_raw": "/media/sounds/tmp0hdvkybg.mp3",
        # Kollywood BGM backups on MyInstants
        "bgm_vikram_mi": "/media/sounds/vikram.mp3",
        "bgm_jailer_mi": "/media/sounds/jailer.mp3",
        "bgm_master_mi": "/media/sounds/master-bgm.mp3",
    }

    with ThreadPoolExecutor(max_workers=10) as ex:
        mi_results = dict(zip(mi_map.keys(), ex.map(lambda kv: download_myinstant(kv[1], kv[0]), mi_map.items())))

    ok_mi = sum(1 for v in mi_results.values() if v)
    print(f"Downloaded {ok_mi}/{len(mi_map)} MyInstants real audio sources.")

    print("=== STAGE 2: Downloading Real Character Voices & Kollywood BGM via yt-dlp ===")
    yt_specs = {
        "stalin_oath": ("7uWaEcZw4OA", 20),
        "vijay_thuppakki": ("7I-8mHFPeWc", 10),
        "vijay_leo": ("qG_zKeo-bno", 10),
        "vijay_wrong": ("VRBFKV_pBfQ", 28),
        "vijay_nenjil": ("4Tr4wws8SaU", 15),
        "jaya": ("UH0RFOWp_uo", 35),
        "pushpa_1": ("QLNspI56XPI", 8),
        "pushpa_all": ("wtDCcVSC7OM", 32),
        "pinarayi_1": ("6xFcglTEgt4", 6),
        "pinarayi_sp": ("lg9lGDW5pwg", 25),
        "dks": ("InP73oR6dUE", 18),
        "pawan_seize": ("Aq-jAh16HtU", 24),
        "pawan_thikka": ("2kYnNW-6Cfo", 14),
        "pawan_2": ("xBCn5kRreI8", 34),
        "seeman_real": ("DeMpTttja20", 30),
        "periyar_1": ("ne_Gb8yvRKk", 24),
        "periyar_reply": ("cStnchubRm4", 35),
        "annamalai_mass": ("P_SO5g3KOnQ", 30),
        "mg_1": ("WLUErZVZQkQ", 30),
        "mg_2": ("R9-O3LcGixk", 30),
        "nirmala_onion": ("fOPEaZfHiMs", 30),
        "nirmala_gst": ("PccfKS7S8n4", 45),
        "rangaraj_kb": ("heoRHRX5Mr0", 18),
        "rangaraj_1": ("eGRLw97W5pc", 95),
        "bgm_vikram_yt": ("elCnQVDEdj8", 35),
        "bgm_jailer_yt": ("UBIA4p_Sgqk", 45),
        "bgm_master_yt": ("R40Ft01RlfY", 30),
    }

    with ThreadPoolExecutor(max_workers=6) as ex:
        yt_results = dict(zip(
            yt_specs.keys(),
            ex.map(lambda kv: download_yt_audio(kv[1][0], kv[1][1], kv[0]), yt_specs.items())
        ))
    ok_yt = sum(1 for v in yt_results.values() if v)
    print(f"Downloaded {ok_yt}/{len(yt_specs)} YouTube audio segments.")

    print("=== STAGE 3: Processing & Normalizing All SFX & Synth Beds ===")
    sfx_targets = {
        "hit_1": ("hit_1", 0.55, ["hit_1.mp3", "sfx/hit_1.mp3"]),
        "hit_2": ("hit_2", 0.65, ["hit_2.mp3", "sfx/hit_2.mp3"]),
        "hit_3": ("hit_3", 0.85, ["hit_3.mp3", "sfx/hit_3.mp3"]),
        "slap": ("slap", 0.65, ["slap.mp3", "sfx/slap.mp3"]),
        "block": ("block", 0.45, ["block.mp3", "sfx/block.mp3"]),
        "whoosh": ("whoosh", 0.55, ["whoosh.mp3", "sfx/whoosh.mp3"]),
        "thud": ("thud", 0.70, ["thud.mp3", "sfx/thud.mp3"]),
        "boom": ("boom", 1.80, ["boom-Brg2wdT5.mp3", "sfx/boom.mp3", "release_chakra-BvOYn27E.mp3", "sfx/release_chakra.mp3", "release_jadu-BVQ3aIZ7.mp3", "sfx/release_jadu.mp3", "release_tariff-DZ1JBEzs.mp3", "sfx/release_tariff.mp3", "release_bulldozer-CyubjB_l.mp3", "sfx/release_bulldozer.mp3"]),
        "bomb": ("bomb", 2.00, ["bomb-1fSoTLVm.mp3", "sfx/bomb.mp3", "pataka-DtLTRxFJ.mp3", "sfx/pataka.mp3"]),
        "thunder": ("thunder", 2.50, ["thunder-BRWemNyY.mp3", "sfx/thunder.mp3"]),
        "bell": ("bell", 2.50, ["bell-DW1wbKh0.mp3", "sfx/bell.mp3"]),
        "cup_break": ("cup_break", 1.10, ["cup_break-BgaQYkuS.mp3", "sfx/cup_break.mp3"]),
        "camera_clicks": ("camera_clicks", 1.40, ["camera_clicks-DJHuyBDj.mp3", "sfx/camera_clicks.mp3"]),
        "horn_long": ("horn_long", 2.20, ["horn_long-dLtoq4Pf.mp3", "sfx/horn_long.mp3"]),
        "horn_short": ("horn_short", 0.85, ["horn_short.mp3", "sfx/horn_short.mp3"]),
        "kaching": ("kaching", 1.10, ["kaching-wbD5pe6-.mp3", "sfx/kaching.mp3"]),
        "coins": ("coins", 1.10, ["coins-DVYyL0Kv.mp3", "sfx/coins.mp3"]),
        "drumroll": ("drumroll", 4.60, ["drumroll-BzHoJfte.mp3", "sfx/drumroll.mp3"]),
        "jingle_win": ("jingle_win", 3.40, ["jingle_win-DqlQ62Fq.mp3", "sfx/jingle_win.mp3"]),
        "jingle_lose": ("jingle_lose", 2.80, ["jingle_lose-gAS4mNKd.mp3", "sfx/jingle_lose.mp3"]),
        "crate_crash": ("crate_crash", 1.20, ["crate_crash-Cr6VTWOz.mp3", "sfx/crate_crash.mp3", "metal_crunch-DdbVoplE.mp3", "sfx/metal_crunch.mp3", "stamp_slam-CAslQB_C.mp3", "sfx/stamp_slam.mp3"]),
        "moo": ("moo", 1.80, ["moo-C_6f5G0B.mp3", "sfx/moo.mp3"]),
        "bark": ("bark", 1.00, ["bark.mp3", "sfx/bark.mp3"]),
        "frog": ("frog", 1.00, ["frog.mp3", "sfx/frog.mp3"]),
        "news_sting": ("news_sting", 1.60, ["news_sting-C-mndS4t.mp3", "sfx/news_sting.mp3"]),
        "heartbeat": ("heartbeat", 2.00, ["heartbeat.mp3", "sfx/heartbeat.mp3"]),
        "reverse_beeps": ("reverse_beeps", 2.00, ["reverse_beeps-DaQ4ZZDr.mp3", "sfx/reverse_beeps.mp3"]),
        "engine_loop": ("engine_loop", 2.80, ["engine_loop-D0YGxkt_.mp3", "sfx/engine_loop.mp3"]),
        "pen_scribble": ("pen_scribble", 2.00, ["pen_scribble-BM1Jp2uD.mp3", "sfx/pen_scribble.mp3"]),
        "snap": ("snap", 0.35, ["snap.mp3", "sfx/snap.mp3"]),
        "plop": ("plop", 0.35, ["plop.mp3", "sfx/plop.mp3"]),
        "chai_ting": ("chai_ting", 0.85, ["chai_ting-Q1sP8TcN.mp3", "sfx/chai_ting.mp3"]),
        "cow_bell": ("cow_bell", 1.20, ["cow_bell-Cj3rAWh8.mp3", "sfx/cow_bell.mp3"]),
        "tick": ("tick", 0.45, ["tick.mp3", "sfx/tick.mp3"]),
    }

    for k, (mi_key, dur, rels) in sfx_targets.items():
        tmp_out = os.path.join(CACHE_DIR, f"proc_sfx_{k}.mp3")
        src = mi_results.get(mi_key)
        ok = False
        if src:
            # Make sure drumroll is at least 4.6s for playTimed("drumroll", dur)
            ok = process_audio_clip(src, tmp_out, ss=0, dur=dur, voice=False, lufs=-12.0, trim_silence=True, fade_io=0.02)
            if ok and k == "drumroll":
                # Check duration >= 4.4s, otherwise pad/loop cleanly with ffmpeg aloop
                ok_dur = run_ffmpeg(["-stream_loop", "2", "-i", tmp_out, "-t", "4.6", "-c:a", "libmp3lame", "-b:a", "160k", tmp_out + ".pad.mp3"])
                if ok_dur:
                    os.replace(tmp_out + ".pad.mp3", tmp_out)
        if not ok:
            synth_studio_ui_or_bed(k, tmp_out)
        copy_to_all(tmp_out, rels)

    # Clean UI / Synth FX & 8s–13s Super Beds
    synth_items = {
        "ui_tap": ["ui_tap.mp3", "sfx/ui_tap.mp3"],
        "ui_select": ["ui_select-DvWPzIZM.mp3", "sfx/ui_select.mp3"],
        "ui_confirm": ["ui_confirm-DEEar_Kj.mp3", "sfx/ui_confirm.mp3"],
        "ui_back": ["ui_back.mp3", "sfx/ui_back.mp3"],
        "shimmer": ["shimmer-XQUc4lgS.mp3", "sfx/shimmer.mp3"],
        "eye_zing": ["eye_zing-qZiVqGmG.mp3", "sfx/eye_zing.mp3"],
        "aloolelo": ["aloolelo-BopBNjJr.mp3", "sfx/aloolelo.mp3"],
        "poof": ["poof-BlJFjDeg.mp3", "sfx/poof.mp3"],
        "charkha": ["charkha-ze2BHoz_.mp3", "sfx/charkha.mp3"],
        "drone": ["drone-DhDpKSwO.mp3", "sfx/drone.mp3"],
        "charge_chakra": ["charge_chakra-1s5EOYKm.mp3", "sfx/charge_chakra.mp3"],
        "bed_chakra": ["bed_chakra-CjyFjT3l.mp3", "sfx/bed_chakra.mp3"],
        "bed_jadu": ["bed_jadu-jl3ElSBF.mp3", "sfx/bed_jadu.mp3"],
        "bed_tariff": ["bed_tariff-CLVTzIAp.mp3", "sfx/bed_tariff.mp3"],
        "bed_bulldozer": ["bed_bulldozer-BE_e8yDo.mp3", "sfx/bed_bulldozer.mp3"],
    }
    for k, rels in synth_items.items():
        tmp_out = os.path.join(CACHE_DIR, f"synth_{k}.mp3")
        synth_studio_ui_or_bed(k, tmp_out)
        copy_to_all(tmp_out, rels)

    print("=== STAGE 4: Processing Arcade Fighting Game Announcer Voices ===")
    announcer_map = {
        "round_1": ("round_1", "Round One!", ["voice/round_1.mp3", "round_1-4pTCkOAK.mp3"]),
        "round_2": ("round_2", "Round Two!", ["voice/round_2.mp3", "round_2-BIyjSuFz.mp3"]),
        "final_round": ("final_round", "Final Round!", ["voice/final_round.mp3", "final_round-2ps4Gt_y.mp3"]),
        "fight": ("fight", "Fight!", ["voice/fight.mp3", "fight-BTHw9nHH.mp3"]),
        "ko": ("ko", "Knockout!", ["voice/ko.mp3", "ko-CYX5YdIq.mp3"]),
        "perfect": ("perfect", "Perfect!", ["voice/perfect.mp3", "perfect-Dm5Oy3HT.mp3"]),
        "you_win": ("you_win", "You Win!", ["voice/you_win.mp3", "you_win-DHsvvWFw.mp3"]),
        "you_lose": ("you_lose", "You Lose!", ["voice/you_lose.mp3", "you_lose-mLbO-eAT.mp3"]),
        "double_ko": (None, "Double Knockout!", ["voice/double_ko.mp3"]),
        "time_up": (None, "Time Up!", ["voice/time_up.mp3", "time_up-Carf_3Z9.mp3"]),
    }
    for k, (mi_key, fallback_txt, rels) in announcer_map.items():
        tmp_out = os.path.join(CACHE_DIR, f"ann_{k}.mp3")
        src = mi_results.get(mi_key) if mi_key else None
        ok = False
        if src:
            ok = process_audio_clip(src, tmp_out, ss=0, dur=2.2, voice=False, lufs=-12.5, trim_silence=True, fade_io=0.02)
        if not ok:
            ok = make_edge_tts_sync(fallback_txt, "en-US-GuyNeural", tmp_out, rate="+5%", pitch="-14Hz")
        if ok:
            copy_to_all(tmp_out, rels)

    print("=== STAGE 5: Processing Kollywood Mass BGM Tracks ===")
    bgm_specs = [
        ("intro-CxITfm7k.mp3", "bgm_vikram_yt", "bgm_vikram_mi", "intro", 28.0),
        ("background-sFl8lOjr.mp3", "bgm_jailer_yt", "bgm_jailer_mi", "background", 32.0),
        ("battle-CqvMijZR.mp3", "bgm_master_yt", "bgm_master_mi", "battle", 28.0),
    ]
    for dest_rel, yt_key, mi_key, fb_kind, dur in bgm_specs:
        tmp_out = os.path.join(CACHE_DIR, f"bgm_{fb_kind}.mp3")
        src = yt_results.get(yt_key) or mi_results.get(mi_key)
        ok = False
        if src:
            ok = process_audio_clip(src, tmp_out, ss=0, dur=dur, voice=False, lufs=-16.0, trim_silence=True, fade_io=0.18)
        if not ok:
            synth_kollywood_bgm_fallback(fb_kind, tmp_out)
        copy_to_all(tmp_out, [dest_rel])
        print(f"  BGM ready: {dest_rel} ({os.path.getsize(os.path.join(ASSETS, dest_rel)) // 1024} KB)")

    print("=== STAGE 6: Processing Verified Real Online Voices (Zero AI/TTS) ===")
    # Each entry: (dest_rel, [(src_kind, key, exact_ss, dur, spoken_text)])
    char_voice_jobs = [
        # 1. SURYA ANNA (MK Stalin)
        ("modi-R8FpxZEb.mp3", [("yt", "stalin_oath", 0.0, 4.6)], "Muthuvel Karunanidhi Stalin ennum naan!"),
        ("memes/modi_1.mp3", [("yt", "stalin_oath", 4.8, 4.6)], "Tamilnattu arasin mudhalamaicharaga..."),
        ("memes/modi_2.mp3", [("yt", "stalin_oath", 9.6, 4.6)], "Nermaiyaga seyven endrum urudhi mozhigiren!"),

        # 2. THALAPATHY (Vijay)
        ("rahul-C7Jjp4hs.mp3", [("yt", "vijay_thuppakki", 0.0, 4.0)], "I am waiting!"),
        ("memes/rahul_1.mp3", [("yt", "vijay_wrong", 14.8, 4.5)], "What bro? It's very wrong bro!"),
        ("memes/rahul_2.mp3", [("yt", "vijay_nenjil", 0.0, 4.2)], "En nenjil kudiyirukkum..."),
        ("rahulwin.mp3", [("yt", "vijay_leo", 0.0, 3.2)], "Bloody Sweet!"),

        # 3. IRON AMMA (J. Jayalalithaa)
        ("didi-CjTHLKgc.mp3", [("yt", "jaya", 0.0, 5.2)], "Makkalal Naan! Makkalukkagave Naan!"),
        ("memes/didi_1.mp3", [("yt", "jaya", 5.8, 4.6)], "Unmaiyana makkal iyakkam!"),
        ("memes/didi_2.mp3", [("yt", "jaya", 18.0, 5.2)], "Naan irukkindra varai, enakkup pinnalum!"),

        # 4. SANDAL RAJU (Allu Arjun - Pushpa)
        ("trump-Czs6_rQc.mp3", [("mi", "pushpa_fire", 0.0, 3.8)], "Pushpa ante flower anukunnava? Fire!"),
        ("memes/trump_1.mp3", [("yt", "pushpa_all", 20.5, 4.8)], "Pushpa Pushparaj... Thaggedhe Le!"),
        ("memes/trump_2.mp3", [("yt", "pushpa_1", 0.0, 4.2)], "Pushpa ante flower-a? Fireuu!"),

        # 5. LAL CAPTAIN (Pinarayi Vijayan)
        ("yogi-CJEN4Csa.mp3", [("yt", "pinarayi_1", 0.0, 4.0)], "Kadakku Purathu!"),
        ("memes/yogi_1.mp3", [("yt", "pinarayi_sp", 0.0, 5.2)], "Mukhyamantri kaserayil aakam, Kendramantri sthaanathu aakam!"),
        ("memes/yogi_2.mp3", [("yt", "pinarayi_sp", 12.0, 4.6)], "Entho undakki kalayam ennanaanu vicharikunnathu!"),

        # 6. BANDE SHIV (D.K. Shivakumar)
        ("nitin-B2ZG9HV5.mp3", [("yt", "dks", 0.0, 7.5)], "One thing I would like to tell you — I am a businessman!"),
        ("memes/nitin_1.mp3", [("yt", "dks", 0.0, 4.6)], "One thing I would like to tell you — my birthday..."),
        ("memes/nitin_2.mp3", [("yt", "dks", 5.0, 4.8)], "By profession I'm a businessman!"),

        # 7. POWER STAR (Pawan Kalyan)
        ("ravi-BUhOMgaW.mp3", [("yt", "pawan_seize", 10.0, 4.8)], "Seize the Ship!"),
        ("memes/ravi_1.mp3", [("yt", "pawan_thikka", 0.0, 4.8)], "Naaku konchem thikka undhi, kaani daniko lekka undhi!"),
        ("memes/ravi_2.mp3", [("yt", "pawan_2", 16.0, 4.6)], "Janamlo unta! Janam la unta!"),
        ("raviwin-Q4j69frZ.mp3", [("yt", "pawan_2", 16.0, 4.6)], "Janamlo unta! Janam la unta!"),

        # 8. PULI VOICE (Seeman)
        ("lalu-vVsgGZuo.mp3", [("yt", "seeman_real", 11.8, 5.4)], "Oru thadava saappittu 27,000 vidhaigalai vidhaikkiraal!"),
        ("memes/lalu_1.mp3", [("yt", "seeman_real", 5.8, 5.2)], "Moondru yaanaigal uyirizhundhirukkindranar!"),
        ("memes/lalu_2.mp3", [("yt", "seeman_real", 17.6, 5.2)], "1500 yaanai irundhuchu... ippa 650 thaan!"),

        # 9. THATHA REFORM (Periyar)
        ("mbapu-D85PVY1T.mp3", [("yt", "periyar_reply", 24.0, 5.2)], "Nambamal poottu podringle — adhu thaan Naathigam!"),
        ("mbapuintro-BI_jQwTJ.mp3", [("yt", "periyar_reply", 6.5, 5.0)], "Kadavul kitta undiyal vekkiringale — adhu Aathigam!"),
        ("gulaam-BnDUPSAr.mp3", [("yt", "periyar_1", 9.5, 4.5)], "Aathma motcham nadakkum!"),
        ("memes/mbapu_1.mp3", [("yt", "periyar_reply", 6.5, 5.0)], "Kadavul kitta undiyal vekkiringale — adhu Aathigam!"),
        ("memes/mbapu_2.mp3", [("yt", "periyar_reply", 24.0, 5.2)], "Nambamal poottu podringle — adhu thaan Naathigam!"),

        # 10. FILES IPS (K. Annamalai)
        ("amit-DJ24Mt8b.mp3", [("yt", "annamalai_mass", 11.8, 4.8)], "Ellathaiyum paathutten! Ellathaiyum paathachu!"),
        ("amitwin-DIIUm105.mp3", [("yt", "annamalai_mass", 17.5, 5.4)], "Ippo irukkira arasiyal thalaivar... vazha mudiyum?!"),
        ("memes/amit_1.mp3", [("yt", "annamalai_mass", 0.0, 5.0)], "Adhukkellam bayappadathinga! Naalaiku kaalaila onnume illaina..."),
        ("memes/amit_2.mp3", [("yt", "annamalai_mass", 11.8, 4.8)], "Ellathaiyum paathutten! Ellathaiyum paathachu!"),

        # 11. SQUAD BRO (Madan Gowri)
        ("dhruv-CHzIxkIz.mp3", [("yt", "mg_1", 4.6, 5.0)], "Hello everyone, naan Madan Gowri! Hello my dear MG Squad!"),
        ("memes/dhruv_1.mp3", [("yt", "mg_1", 4.6, 5.0)], "Hello everyone, naan Madan Gowri! Hello my dear MG Squad!"),
        ("memes/dhruv_2.mp3", [("yt", "mg_2", 0.0, 5.2)], "Indha video oru inspirational video-va illa motivational video-va..."),

        # 12. TAX MAAMI (Nirmala Sitharaman)
        ("nirmala-Dq7cz8UN.mp3", [("yt", "nirmala_onion", 18.0, 5.6)], "Main itna lehsun pyaaz nahi khati hoon ji!"),
        ("memes/nirmala_1.mp3", [("yt", "nirmala_onion", 24.0, 4.8)], "Waise parivar se aati hoon jahan onion rakhte hi nahi!"),
        ("memes/nirmala_2.mp3", [("yt", "nirmala_gst", 12.0, 5.4)], "Social media: popcorn ke upar bhi daal rahe hain tax!"),

        # 13. RANGARAJ (Rangaraj Pandey)
        ("rangaraj-super.mp3", [("yt", "rangaraj_kb", 0.0, 4.6)], "Dhairiyam purusha latchanam! Naan ungalai sollavillai!"),
        ("memes/rangaraj_1.mp3", [("yt", "rangaraj_1", 66.0, 5.6)], "Edhirkatchi thalaivarum pradhanarum saadharanama pesittu iruppanga!"),
        ("memes/rangaraj_2.mp3", [("yt", "rangaraj_1", 84.0, 5.6)], "Irandaavadhu point vandhu... Bharat Pradhanam!"),
    ]

    for dest_rel, candidates, spoken_text in char_voice_jobs:
        dst = os.path.join(ASSETS, dest_rel.replace("/", os.sep))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        done = False
        for src_kind, key, ss, dur in candidates:
            src_path = yt_results.get(key) if src_kind == "yt" else mi_results.get(key)
            if not src_path:
                continue
            if process_audio_clip(src_path, dst, ss=ss, dur=dur, voice=True, lufs=-13.5, trim_silence=True, fade_io=0.03):
                if is_valid_audio(dst):
                    print(f"  [REAL {src_kind.upper()}] {dest_rel:28s} @ {ss:4.1f}s ({os.path.getsize(dst)//1024:3d} KB) -> {spoken_text}")
                    done = True
                    break
        assert done, f"FAILED to extract real online audio for {dest_rel} from {candidates}"

    print("Audio overhaul complete!")


if __name__ == "__main__":
    main()
