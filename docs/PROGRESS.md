# Dakshin Showdown — Playbook Progress Log

## Baseline
- **Initial Baseline Commit:** `16ac92d` (`chore: baseline before improvement playbook Wave 0`)

## Wave 0 — Foundation (Complete)
- **Status:** `PASS` (`scripts/verify.py` exited `0` in `~2.1s`, `0` failures)
- **Key Deliverables:**
  - `.gitignore` + Git baseline initialized (`git init`).
  - `scripts/patch_south.py` refactored into 7 modular files under `scripts/patches/`:
    - `scripts/patches/context.py` (report-and-continue `PatchContext`; collects all missed anchors and exits non-zero at the end rather than halting at first miss)
    - `01_imports_and_ga.py`
    - `02_stages_and_crowd.py`
    - `03_roster_and_models.py`
    - `04_audio_and_voices.py`
    - `05_dialogues_and_supers.py`
    - `06_combat_and_assists.py`
    - `07_ui_and_hud.py`
  - Removed hardcoded `brain\...` conversation UUID paths from `scripts/overhaul_audio.py` (`--cache-dir` / `DAKSHIN_AUDIO_CACHE`) and `scripts/reconstruct.py` (`--out-dir` / `DAKSHIN_RECONSTRUCT_DIR`).
  - Added `scripts/verify.py` implementing all 6 checks (patch pipeline, JS syntax across `public/assets/*.js`, referenced asset existence, uniqueness warnings, ephemeral-port HTTP 200 smoke test, North leftover warnings).

## Known Wave 1 Targets Flagged by `verify.py` (`WARN`)
- **V1:** `public/faces/amit.webp` and `public/faces/rangaraj.webp` are byte-identical (`md5: 3860b8b88da05e1c1c70ced642cc2370`).
- **A1:** Duplicate super SFX (`release_bulldozer == release_chakra == release_jadu == release_tariff`, `bed_bulldozer == bed_tariff`, `bed_chakra == charge_chakra`).
- **A2:** Duplicate hashed + unhashed SFX pairs (`/assets/<name>-<hash>.mp3` vs `/assets/sfx/<name>.mp3`).
- **V2:** 13 `models/mobile/*.glb` files identical to `models/*.glb`; legacy `bull1.glb`, `shepherd.glb`, `Fighter3D.js`, `GameEngine3D.js`.
- **C1:** Missing `docs/ID_MAP.md` single source of truth mapping legacy internal IDs (`modi`, `rahul`, ...) to Pan-South characters.
