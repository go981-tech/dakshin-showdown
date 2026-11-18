import argparse
import json
import os
import re

OUT_DIR = os.environ.get("DAKSHIN_RECONSTRUCT_DIR", "")
DEST_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "public", "assets")
os.makedirs(DEST_DIR, exist_ok=True)


def load_step(num):
    with open(os.path.join(OUT_DIR, f"step_{num}.json"), encoding="utf-8") as f:
        return json.load(f)["value"]


def fix_mojibake(text: str) -> str:
    # Browser DOM textContent / innerHTML of UTF-8 JS served without charset=utf-8
    # sometimes produces Latin-1/Windows-1252 mojibake like 'Â·' or 'â€”'.
    # Re-encode per-segment if possible.
    def _fix_match(m):
        s = m.group(0)
        try:
            return s.encode("cp1252").decode("utf-8")
        except Exception:
            try:
                return s.encode("latin1").decode("utf-8")
            except Exception:
                return s

    # Match runs of non-ASCII chars that look like UTF-8 decoded as cp1252/latin1
    # Specifically strings containing Ã, Â, â, ðŸ, etc.
    out = []
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if ord(ch) > 127:
            # try greedy UTF-8 sequence length 2, 3, 4 decoded via cp1252
            fixed = False
            for length in (4, 3, 2):
                if i + length <= n:
                    sub = text[i : i + length]
                    try:
                        b = sub.encode("cp1252")
                        dec = b.decode("utf-8")
                        if len(dec) == 1:
                            out.append(dec)
                            i += length
                            fixed = True
                            break
                    except Exception:
                        pass
                    try:
                        b = sub.encode("latin1")
                        dec = b.decode("utf-8")
                        if len(dec) == 1:
                            out.append(dec)
                            i += length
                            fixed = True
                            break
                    except Exception:
                        pass
            if not fixed:
                out.append(ch)
                i += 1
        else:
            out.append(ch)
            i += 1
    return "".join(out)


def stitch_exact(parts):
    """Concatenate chunks, removing any exact suffix/prefix overlap if present."""
    res = parts[0]
    for nxt in parts[1:]:
        # Check overlap up to 200 chars
        overlap = 0
        max_ov = min(200, len(res), len(nxt))
        for k in range(max_ov, 0, -1):
            if res.endswith(nxt[:k]):
                overlap = k
                break
        res += nxt[overlap:]
    return res


def reconstruct_css():
    chunks = [
        load_step(66)["cssChunk0"],
        load_step(76)["chunk"],
        load_step(78)["chunk"],
        load_step(80)["chunk"],
        load_step(82)["chunk"],
        load_step(84)["chunk"],
        load_step(86)["chunk"],
        load_step(88)["cssTail"],
    ]
    css = stitch_exact(chunks)
    css = fix_mojibake(css)
    path = os.path.join(DEST_DIR, "main-BAhoKV_T.css")
    with open(path, "w", encoding="utf-8") as f:
        f.write(css)
    print(f"CSS written: {len(css)} chars -> {path}")


def reconstruct_rooms():
    chunks = [
        load_step(70)["roomsHead"],
        load_step(72)["chunk"],
        load_step(76)["roomsTail"],
    ]
    rooms = stitch_exact(chunks)
    rooms = fix_mojibake(rooms)
    path = os.path.join(DEST_DIR, "rooms-CujU6IZK.js")
    with open(path, "w", encoding="utf-8") as f:
        f.write(rooms)
    print(f"rooms.js written: {len(rooms)} chars -> {path}")


def reconstruct_main():
    # Inline sfx map from step_106 midClean:
    # var Yn=`data:audio/mpeg;base64,<OMITTED len=3807>` etc.
    # Map them directly to /assets/sfx_...mp3 or silent/synthesized WAV files we generate
    s90 = load_step(90)["chunk"]
    s94 = load_step(94)["chunk"]
    s96 = load_step(96)["chunk"]
    s98 = load_step(98)["chunk"]
    s104 = load_step(104)["chunk"]

    s106 = load_step(106)
    pre = s106["pre"]
    mid = s106["midClean"]
    post = s106["post"]

    # Map each variable in midClean to a clean asset path that generate_assets.js will create!
    # Look at oi in post:
    # bark:Yn, block:tr, frog:gr, heartbeat:_r, hit_1:vr, hit_2:yr, hit_3:br, horn_short:Sr,
    # plop:jr, slap:zr, snap:Br, thud:Hr, tick:Wr, ui_back:Gr, ui_tap:Jr, whoosh:Yr
    inline_var_to_path = {
        "Yn": "/assets/bark.mp3",
        "tr": "/assets/block.mp3",
        "gr": "/assets/frog.mp3",
        "vr": "/assets/hit_1.mp3",
        "_r": "/assets/heartbeat.mp3",
        "yr": "/assets/hit_2.mp3",
        "br": "/assets/hit_3.mp3",
        "Sr": "/assets/horn_short.mp3",
        "jr": "/assets/plop.mp3",
        "zr": "/assets/slap.mp3",
        "Br": "/assets/snap.mp3",
        "Hr": "/assets/thud.mp3",
        "Wr": "/assets/tick.mp3",
        "Gr": "/assets/ui_back.mp3",
        "Jr": "/assets/ui_tap.mp3",
        "Yr": "/assets/whoosh.mp3",
    }

    for var, url in inline_var_to_path.items():
        pattern = rf"{re.escape(var)}=`data:audio/mpeg;base64,<OMITTED len=\d+>`"
        mid = re.sub(pattern, f"{var}=`{url}`", mid)

    # Also remove the partial 'data:audio/mpeg;base64,SUQzBAAAAAAAIlRTU0U' at end of pre
    # and 'VVVVQ==`' at start of post, or let mid handle from Yn= to Xr=
    # Let's inspect pre/mid/post stitch carefully:
    # pre ends with: Jn=`/assets/aloolelo-BopBNjJr.mp3`,Yn=`data:audio/mpeg;base64,SUQzBAAAAAAAIlRTU0U
    # mid starts with: BopBNjJr.mp3`,Yn=`/assets/bark.mp3`,... and ends with ,Yr=`/assets/whoosh.mp3`,Xr=`/assets/ko-C
    # post starts with: VVVVQ==`,Xr=`/assets/ko-CYX5YdIq.mp3`,...
    pre_cut = pre[: pre.rfind("BopBNjJr.mp3`")]
    mid_clean_part = mid
    # Strip trailing incomplete Xr=`/assets/ko-C from mid and leading VVVVQ==` from post
    mid_cut = mid_clean_part[: mid_clean_part.rfind(",Xr=`")]
    post_cut = post[post.find(",Xr=`") :]
    s106_joined = pre_cut + mid_cut + post_cut

    parts = [s90, s94, s96, s98, s104]
    base_prefix = stitch_exact(parts)
    # s104 ends around 45100, pre_cut starts at 45100
    full = stitch_exact([base_prefix, s106_joined])

    s108 = load_step(108)["chunk"]
    full = stitch_exact([full, s108])

    for step_num in range(110, 138, 2):
        full = stitch_exact([full, load_step(step_num)["c"]])

    for step_num in [141, 143, 145, 147, 149, 151, 153, 155, 157, 159, 161, 163, 165, 167, 169, 171, 173]:
        full = stitch_exact([full, load_step(step_num)["c"]])

    for step_num in range(178, 206, 2):
        full = stitch_exact([full, load_step(step_num)["c"]])

    # Verify if there are any omitted placeholders left
    assert "<OMITTED" not in full, "Found leftover OMITTED placeholder!"

    full = fix_mojibake(full)

    path = os.path.join(DEST_DIR, "main-C7-oASSx.js")
    with open(path, "w", encoding="utf-8") as f:
        f.write(full)
    print(f"main.js written: {len(full)} chars -> {path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reconstruct bundled assets from browser snapshot outputs.")
    parser.add_argument("--out-dir", default=OUT_DIR, help="Path to captured browser_sandbox/outputs directory (or set DAKSHIN_RECONSTRUCT_DIR)")
    args = parser.parse_args()
    if not args.out_dir or not os.path.isdir(args.out_dir):
        raise SystemExit("Provide a valid --out-dir or set DAKSHIN_RECONSTRUCT_DIR")
    OUT_DIR = os.path.abspath(args.out_dir)
    reconstruct_css()
    reconstruct_rooms()
    reconstruct_main()
