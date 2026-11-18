#!/usr/bin/env python3
"""
Verification suite for Dakshin Showdown (runs in <30s).
Implements Part 4 of improvement_playbook.md:
  1. Patch pipeline (patch_south.py) with 0 failed anchors
  2. node --check on every .js in public/assets/
  3. Asset existence check across HTML, CSS, JS
  4. Uniqueness checks (faces, super SFX beds/releases, mobile GLBs) -> WARN in Wave 0
  5. HTTP server smoke test on ephemeral free port (/ + 20 random assets -> 200 OK)
  6. Banned North leftover string check -> WARN
  7. Summary table: CHECK | STATUS | DETAIL
"""

import glob
import hashlib
import os
import random
import re
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC = os.path.join(ROOT, "public")
ASSETS = os.path.join(PUBLIC, "assets")


def md5_file(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def check_patch_pipeline():
    p = subprocess.run(
        [sys.executable, os.path.join(ROOT, "scripts", "patch_south.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=20,
    )
    if p.returncode != 0:
        tail = (p.stdout + "\n" + p.stderr).strip().splitlines()[-5:]
        return ("FAIL", f"exit {p.returncode}: {' | '.join(tail)}")
    return ("PASS", "all patch modules applied with 0 failures")


def check_js_syntax():
    js_files = sorted(glob.glob(os.path.join(ASSETS, "*.js")))
    if not js_files:
        return ("FAIL", "no .js files found in public/assets/")
    failed = []
    for jf in js_files:
        res = subprocess.run(
            ["node", "--check", jf],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=10,
        )
        if res.returncode != 0:
            failed.append(f"{os.path.basename(jf)}: {res.stderr.strip()[:120]}")
    if failed:
        return ("FAIL", "; ".join(failed))
    return ("PASS", f"{len(js_files)} JS files passed node --check")


def collect_referenced_assets():
    refs = set()
    scan_files = [os.path.join(PUBLIC, "index.html")]
    scan_files += sorted(glob.glob(os.path.join(ASSETS, "*.css")))
    scan_files += sorted(glob.glob(os.path.join(ASSETS, "*.js")))

    # Regex handles static literal paths starting with /assets/, /characters/, /faces/, /models/
    # and ignores JS template literals containing ${
    pat = re.compile(r"""(?:["'`(])(/(?:assets|characters|faces|models)/[^"'`)\s?\\]+)""")
    # Also handle relative facePhoto refs like faces/<id>.webp in Roster/patch outputs
    rel_face_pat = re.compile(r"""[`"'](faces/[a-zA-Z0-9_/\-]+\.(?:webp|png|jpg))[`"'\?]""")

    for fp in scan_files:
        if not os.path.exists(fp):
            continue
        with open(fp, "r", encoding="utf-8", errors="ignore") as f:
            txt = f.read()
        for m in pat.finditer(txt):
            url = m.group(1)
            if "${" in url or url.endswith("/"):
                continue
            # Ignore internal source regexes or fake bundle keys if not concrete file paths
            if url.endswith((".js", ".css", ".mp3", ".webp", ".png", ".jpg", ".glb", ".svg", ".json")):
                refs.add(url)
        for m in rel_face_pat.finditer(txt):
            rel = "/" + m.group(1)
            if "${" not in rel:
                refs.add(rel)
    return sorted(refs)


def check_asset_existence(refs):
    missing = []
    for u in refs:
        rel = u.lstrip("/").replace("/", os.sep)
        full = os.path.join(PUBLIC, rel)
        if not os.path.isfile(full):
            missing.append(u)
    if missing:
        return ("FAIL", f"{len(missing)} missing assets (e.g. {', '.join(missing[:5])})")
    return ("PASS", f"{len(refs)} referenced assets verified on disk")


def check_uniqueness():
    issues = []

    # 1. Main fighter faces/*.webp (excluding *_uv.webp texture maps)
    face_hashes = {}
    for fp in sorted(glob.glob(os.path.join(PUBLIC, "faces", "*.webp"))):
        name = os.path.basename(fp)
        if "_uv." in name:
            continue
        h = md5_file(fp)
        face_hashes.setdefault(h, []).append(name)
    dup_faces = [v for v in face_hashes.values() if len(v) > 1]
    if dup_faces:
        issues.append(f"duplicate faces: {dup_faces}")

    # 2. Super SFX (release_*, charge_*, bed_*) in public/assets/sfx/
    sfx_hashes = {}
    for fp in sorted(glob.glob(os.path.join(ASSETS, "sfx", "*.mp3"))):
        name = os.path.basename(fp)
        if name.startswith(("release_", "charge_", "bed_")):
            h = md5_file(fp)
            sfx_hashes.setdefault(h, []).append(name)
    dup_sfx = [v for v in sfx_hashes.values() if len(v) > 1]
    if dup_sfx:
        issues.append(f"duplicate super SFX: {dup_sfx}")

    # 3. Mobile GLBs vs Desktop GLBs
    mob_same = []
    for fp in sorted(glob.glob(os.path.join(PUBLIC, "models", "mobile", "*.glb"))):
        name = os.path.basename(fp)
        desk = os.path.join(PUBLIC, "models", name)
        if os.path.isfile(desk) and md5_file(fp) == md5_file(desk):
            mob_same.append(name)
    if mob_same:
        issues.append(f"mobile/*.glb identical to desktop ({len(mob_same)} files)")

    if issues:
        return ("WARN", " | ".join(issues))
    return ("PASS", "all checked faces, super SFX, and mobile GLBs are unique")


def check_http_server(refs):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]

    env = dict(os.environ)
    env["PORT"] = str(port)
    proc = subprocess.Popen(
        ["node", os.path.join(ROOT, "server.js")],
        cwd=ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    try:
        # Wait up to 5s for server to bind
        ready = False
        deadline = time.time() + 5.0
        while time.time() < deadline:
            if proc.poll() is not None:
                return ("FAIL", f"server.js exited early ({proc.returncode})")
            try:
                with socket.create_connection(("127.0.0.1", port), timeout=0.25):
                    ready = True
                    break
            except OSError:
                time.sleep(0.1)

        if not ready:
            return ("FAIL", f"server.js did not open port {port} within 5s")

        rng = random.Random(42)
        sample = rng.sample(refs, min(20, len(refs))) if refs else []
        targets = ["/"] + sample
        bad = []
        for path in targets:
            url = f"http://127.0.0.1:{port}{path}"
            try:
                with urllib.request.urlopen(url, timeout=3.0) as resp:
                    if resp.status != 200:
                        bad.append(f"{path} -> HTTP {resp.status}")
            except urllib.error.HTTPError as e:
                bad.append(f"{path} -> HTTP {e.code}")
            except Exception as e:
                bad.append(f"{path} -> {e}")

        if bad:
            return ("FAIL", f"{len(bad)} failed HTTP GETs: {', '.join(bad[:4])}")
        return ("PASS", f"HTTP 200 for / + {len(sample)} sampled assets on port {port}")
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            proc.kill()


def check_leftovers():
    terms = ["SANSAD", "JANTAR MANTAR", "NEW DELHI", "जंतर"]
    scan_files = [os.path.join(PUBLIC, "index.html")]
    scan_files += sorted(glob.glob(os.path.join(ASSETS, "*.css")))
    scan_files += sorted(glob.glob(os.path.join(ASSETS, "*.js")))
    hits = {}
    for fp in scan_files:
        base = os.path.basename(fp)
        with open(fp, "r", encoding="utf-8", errors="ignore") as f:
            txt = f.read()
        for t in terms:
            c = len(re.findall(re.escape(t), txt, re.IGNORECASE))
            if t == "SANSAD":
                # Exclude internal localStorage key sansad-showdown
                c -= len(re.findall(r"sansad-showdown", txt, re.IGNORECASE))
            if c > 0:
                hits.setdefault(base, []).append(f"{t}:{c}")
    if hits:
        summary = "; ".join(f"{k}({','.join(v)})" for k, v in sorted(hits.items()))
        return ("WARN", summary)
    return ("PASS", "no North leftover strings found")


def main():
    t0 = time.time()
    refs = collect_referenced_assets()

    checks = [
        ("1. Patch pipeline", check_patch_pipeline()),
        ("2. JS syntax", check_js_syntax()),
        ("3. Asset existence", check_asset_existence(refs)),
        ("4. Uniqueness guards", check_uniqueness()),
        ("5. HTTP smoke test", check_http_server(refs)),
        ("6. North leftovers", check_leftovers()),
    ]

    print(f"{'CHECK':22s} | {'STATUS':6s} | DETAIL")
    print("-" * 22 + "-+-" + "-" * 6 + "-+-" + "-" * 50)
    fails = 0
    for name, (status, detail) in checks:
        if status == "FAIL":
            fails += 1
        print(f"{name:22s} | {status:6s} | {detail}")

    elapsed = time.time() - t0
    print(f"\nCompleted in {elapsed:.2f}s (failures: {fails})")
    return 1 if fails > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
