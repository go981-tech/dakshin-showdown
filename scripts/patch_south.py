#!/usr/bin/env python3
"""
Modular patch runner for Dakshin Showdown.
Rebuilds public/assets/main-C7-oASSx.js from public/assets/main-C7-oASSx.js.bak
by running scripts/patches/NN_*.py in sorted order with report-and-continue diagnostics.
"""

import importlib
import os
import pkgutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from scripts.patches.context import PatchContext
import scripts.patches as patches_pkg

JS_PATH = os.path.join(ROOT, "public", "assets", "main-C7-oASSx.js")
BAK_PATH = JS_PATH + ".bak"


def run_all(write_output: bool = True):
    if not os.path.exists(BAK_PATH):
        raise FileNotFoundError(f"Missing baseline backup file: {BAK_PATH}")

    with open(BAK_PATH, "r", encoding="utf-8", newline="") as f:
        src = f.read()

    ctx = PatchContext(src)
    mod_names = sorted(
        m.name
        for m in pkgutil.iter_modules(patches_pkg.__path__)
        if m.name != "context" and not m.name.startswith("_")
    )

    per_module = []
    for name in mod_names:
        ctx.set_module(name)
        before_idx = len(ctx.records)
        mod = importlib.import_module(f"scripts.patches.{name}")
        mod.apply(ctx)
        recs = ctx.records[before_idx:]
        passed = sum(1 for r in recs if r["ok"])
        failed = len(recs) - passed
        per_module.append((name, passed, failed))

    print("MODULE                     | PASS | FAIL")
    print("---------------------------+------+-----")
    for name, passed, failed in per_module:
        print(f"{name:26s} | {passed:4d} | {failed:4d}")

    fails = ctx.failures()
    if fails:
        print("\nFAILED ANCHORS:")
        for r in fails:
            print(f"  [{r['module']}] {r['label']}: {r['detail']}")
        return False

    if write_output:
        out_text = ctx.src.replace("\r\n", "\n")
        with open(JS_PATH, "w", encoding="utf-8", newline="\n") as f:
            f.write(out_text)
        print(f"\nSuccessfully patched {JS_PATH} ({len(out_text)} chars)")
    return True


if __name__ == "__main__":
    ok = run_all(write_output=True)
    sys.exit(0 if ok else 1)
