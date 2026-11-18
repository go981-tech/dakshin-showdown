import io
import json
import math
import os
import shutil
import struct
import urllib.request
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC = os.path.join(ROOT, "public")
SCRIPTS = os.path.join(ROOT, "scripts")
FACES_DIR = os.path.join(PUBLIC, "faces")
ART_DIR = os.path.join(PUBLIC, "art")
ART_MOBILE_DIR = os.path.join(ART_DIR, "mobile")
MODELS_DIR = os.path.join(PUBLIC, "models")
MOBILE_MODELS_DIR = os.path.join(MODELS_DIR, "mobile")

os.makedirs(FACES_DIR, exist_ok=True)
os.makedirs(ART_DIR, exist_ok=True)
os.makedirs(ART_MOBILE_DIR, exist_ok=True)
os.makedirs(MOBILE_MODELS_DIR, exist_ok=True)

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"

FIGHTER_IDS = ["modi", "rahul", "didi", "yogi", "trump", "nitin", "ravi", "lalu", "mbapu", "amit", "dhruv"]
EXTRA_GLBS = ["bull1", "shepherd"]

# 100% Stylized Cartoon Character Blueprints (ZERO real-person photographs!)
FIGHTER_SPECS = {
    "modi": {
        "base": "modi",
        "skin": (178, 126, 94),
        "hair": (22, 22, 28),
        "hair_style": "side_silver",
        "mustache": "trim",
        "beard": "none",
        "glasses": "rim",
        "tilak": "none",
        "smile": "warm",
        "bg": [(127, 29, 29), (24, 14, 24)],
        "accent": (250, 204, 21),
        "top_tint": (244, 242, 236),
        "bottom_tint": (244, 242, 236),
        "bottom_border": [(208, 22, 34), (24, 24, 28)],
        "shawl_colors": [(208, 22, 34), (24, 24, 28)],
    },
    "rahul": {
        "base": "rahul",
        "skin": (196, 144, 110),
        "hair": (20, 20, 26),
        "hair_style": "quiff",
        "mustache": "thick",
        "beard": "stubble_goatee",
        "glasses": "shades",
        "tilak": "none",
        "smile": "smirk",
        "bg": [(153, 27, 27), (30, 10, 16)],
        "accent": (250, 204, 21),
        "top_tint": (246, 244, 238),
        "bottom_tint": (48, 50, 58),
        "shawl_colors": [(198, 28, 34), (246, 200, 28)],
    },
    "didi": {
        "base": "didi",
        "skin": (214, 166, 140),
        "hair": (18, 18, 24),
        "hair_style": "bun",
        "mustache": "none",
        "beard": "none",
        "glasses": "none",
        "tilak": "pottu",
        "smile": "regal",
        "bg": [(6, 95, 70), (14, 34, 24)],
        "accent": (250, 204, 21),
        "top_tint": (11, 110, 60),
        "bottom_tint": (11, 110, 60),
        "sari_border": (235, 182, 40),
    },
    "trump": {
        "base": "rahul",
        "skin": (182, 128, 92),
        "hair": (22, 18, 18),
        "hair_style": "curly_mass",
        "mustache": "wild",
        "beard": "full",
        "glasses": "shades",
        "tilak": "none",
        "smile": "fierce",
        "bg": [(194, 65, 12), (42, 16, 10)],
        "accent": (251, 146, 60),
        "top_tint": (214, 92, 38),
        "pushpa_floral": True,
        "clean_collar": True,
        "bottom_tint": (36, 34, 38),
    },
    "yogi": {
        "base": "modi",
        "skin": (188, 138, 106),
        "hair": (224, 224, 232),
        "hair_shade": 0.92,
        "hair_style": "receding_silver",
        "mustache": "bushy_white",
        "beard": "none",
        "glasses": "rimless",
        "tilak": "none",
        "smile": "stern",
        "bg": [(153, 27, 27), (26, 8, 12)],
        "accent": (248, 113, 113),
        "top_tint": (244, 242, 238),
        "bottom_tint": (244, 242, 238),
        "bottom_border": [(212, 172, 62), (185, 28, 32)],
        "shawl_colors": [(204, 26, 30), (235, 228, 210)],
    },
    "nitin": {
        "base": "modi",
        "skin": (192, 142, 110),
        "hair": (34, 34, 42),
        "hair_style": "salt_pepper",
        "mustache": "salt_pepper",
        "beard": "salt_pepper",
        "glasses": "none",
        "tilak": "vibhuti",
        "smile": "bold",
        "bg": [(3, 105, 161), (12, 26, 48)],
        "accent": (56, 189, 248),
        "top_tint": (242, 240, 234),
        "top_jacket_tint": (24, 52, 88),
        "bottom_tint": (240, 238, 232),
    },
    "ravi": {
        "base": "rahul",
        "skin": (182, 130, 96),
        "hair": (18, 18, 22),
        "hair_style": "windswept",
        "mustache": "handlebar",
        "beard": "trimmed",
        "glasses": "shades",
        "tilak": "red_tilak",
        "smile": "smirk",
        "bg": [(185, 28, 28), (24, 12, 22)],
        "accent": (248, 113, 113),
        "top_tint": (244, 242, 236),
        "bottom_tint": (242, 240, 234),
        "shawl_colors": [(206, 26, 28), (242, 240, 234)],
    },
    "lalu": {
        "base": "rahul",
        "skin": (174, 122, 92),
        "hair": (18, 18, 24),
        "hair_style": "swept",
        "mustache": "handlebar",
        "beard": "none",
        "glasses": "none",
        "tilak": "none",
        "smile": "shouting",
        "bg": [(180, 83, 9), (42, 10, 12)],
        "accent": (250, 204, 21),
        "top_tint": (228, 174, 38),
        "bottom_tint": (242, 240, 232),
        "bottom_border": [(196, 26, 26), (236, 190, 32)],
        "shawl_colors": [(196, 26, 26), (242, 194, 30)],
    },
    "mbapu": {
        "base": "modi",
        "skin": (176, 128, 96),
        "hair": (228, 228, 236),
        "hair_shade": 0.94,
        "hair_style": "flowing_white",
        "mustache": "white_long",
        "beard": "long_white",
        "glasses": "round",
        "tilak": "none",
        "smile": "wise",
        "bg": [(39, 39, 42), (12, 12, 16)],
        "accent": (250, 204, 21),
        "top_tint": (26, 26, 30),
        "bottom_tint": (26, 26, 30),
        "bottom_border": [(240, 198, 42), (24, 24, 28)],
        "shawl_colors": [(185, 28, 32), (24, 24, 28)],
    },
    "amit": {
        "base": "rahul",
        "skin": (178, 126, 92),
        "hair": (18, 18, 24),
        "hair_style": "dense_crop",
        "mustache": "thick",
        "beard": "full",
        "glasses": "shades",
        "tilak": "red_tilak",
        "smile": "stern",
        "bg": [(234, 88, 12), (40, 14, 10)],
        "accent": (251, 146, 60),
        "top_tint": (242, 240, 234),
        "bottom_tint": (242, 240, 234),
        "bottom_border": [(242, 118, 24), (242, 240, 234)],
        "shawl_colors": [(242, 114, 22), (252, 168, 46)],
    },
    "dhruv": {
        "base": "rahul",
        "skin": (198, 146, 112),
        "hair": (20, 20, 26),
        "hair_style": "tall_quiff",
        "mustache": "stubble",
        "beard": "stubble_goatee",
        "glasses": "headphones",
        "tilak": "none",
        "smile": "warm",
        "bg": [(14, 116, 144), (8, 26, 48)],
        "accent": (34, 211, 238),
        "top_tint": (22, 64, 86),
        "clean_collar": True,
        "bottom_tint": (186, 174, 152),
    },
}


def download_glb(name):
    mob_path = os.path.join(MOBILE_MODELS_DIR, f"{name}.glb")
    desk_path = os.path.join(MODELS_DIR, f"{name}.glb")
    if not os.path.exists(mob_path) or os.path.getsize(mob_path) < 50000:
        url = f"https://fightkaro.com/models/mobile/{name}.glb"
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
        with open(mob_path, "wb") as f:
            f.write(data)
        print(f"  Downloaded {name}.glb ({len(data)} bytes)")
    if not os.path.exists(desk_path) or os.path.getsize(desk_path) != os.path.getsize(mob_path):
        shutil.copy2(mob_path, desk_path)
    return mob_path


def extract_glb_textures(glb_path, want_names):
    with open(glb_path, "rb") as f:
        data = f.read()
    jlen, _ = struct.unpack("<II", data[12:20])
    j = json.loads(data[20 : 20 + jlen].decode("utf-8"))
    bin_data = data[20 + jlen + 8 :]
    out = {}
    for m in j.get("materials", []):
        mname = m.get("name", "")
        if mname not in want_names:
            continue
        bct = m.get("pbrMetallicRoughness", {}).get("baseColorTexture", {})
        if "index" not in bct:
            continue
        tex = j["textures"][bct["index"]]
        i_idx = tex.get("source", tex.get("extensions", {}).get("EXT_texture_webp", {}).get("source"))
        bv = j["bufferViews"][j["images"][i_idx]["bufferView"]]
        raw = bin_data[bv.get("byteOffset", 0) : bv.get("byteOffset", 0) + bv["byteLength"]]
        out[mname] = Image.open(io.BytesIO(raw)).convert("RGB")
    return out


def build_head_3d_masks(base_key):
    """Rasterize exact 3D-space semantic masks (hair_mask, mouth_mask) from uvmesh JSON."""
    mesh_path = os.path.join(SCRIPTS, f"uvmesh_{base_key}.json")
    data = json.load(open(mesh_path, "r", encoding="utf-8"))["Head"]
    pts, tris = data["pts"], data["tris"]

    hair_im = Image.new("L", (1024, 1024), 0)
    hair_receding_im = Image.new("L", (1024, 1024), 0)
    mouth_im = Image.new("L", (1024, 1024), 0)
    hd, hrd, md = ImageDraw.Draw(hair_im), ImageDraw.Draw(hair_receding_im), ImageDraw.Draw(mouth_im)

    for i0, i1, i2 in tris:
        p0, p1, p2 = pts[i0], pts[i1], pts[i2]
        cx = (p0[0] + p1[0] + p2[0]) / 3.0
        cy = (p0[1] + p1[1] + p2[1]) / 3.0
        cz = (p0[2] + p1[2] + p2[2]) / 3.0
        cu = (p0[3] + p1[3] + p2[3]) / 3.0
        cv = (p0[4] + p1[4] + p2[4]) / 3.0
        xy = [(p0[3] * 1024.0, p0[4] * 1024.0), (p1[3] * 1024.0, p1[4] * 1024.0), (p2[3] * 1024.0, p2[4] * 1024.0)]

        if cv > 0.875 and (cu < 0.105 or cu > 0.895) and cy < 1.635:
            md.polygon(xy, fill=255)
            continue

        if abs(cx) > 0.065 and (-0.032 < cz < 0.038) and (1.56 < cy < 1.690):
            continue

        if cz >= 0.03:
            y_cut = 1.724 - 0.40 * max(0.0, abs(cx) - 0.038)
            y_cut_rec = 1.752 - 0.35 * max(0.0, abs(cx) - 0.048)
        elif cz > -0.02:
            t_z = (0.03 - cz) / 0.05
            y_cut = 1.710 * (1.0 - t_z) + 1.645 * t_z
            y_cut_rec = 1.740 * (1.0 - t_z) + 1.655 * t_z
        else:
            t_back = min(1.0, (-0.02 - cz) / 0.05)
            y_cut = 1.645 * (1.0 - t_back) + 1.555 * t_back
            y_cut_rec = 1.655 * (1.0 - t_back) + 1.565 * t_back

        is_sideburn = (-0.008 < cz < 0.032) and (1.618 < cy < 1.672) and (abs(cx) > 0.063)
        if cy >= y_cut or is_sideburn:
            hd.polygon(xy, fill=255)
        if cy >= y_cut_rec:
            hrd.polygon(xy, fill=255)

    hair_im = hair_im.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(7))
    hair_receding_im = hair_receding_im.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(7))
    mouth_im = mouth_im.filter(ImageFilter.MaxFilter(3))
    return hair_im, hair_receding_im, mouth_im


def build_vest_uv_mask():
    mesh_path = os.path.join(SCRIPTS, "uvmesh_modi.json")
    data = json.load(open(mesh_path, "r", encoding="utf-8"))["OutfitTop"]
    pts, tris = data["pts"], data["tris"]
    im = Image.new("L", (512, 512), 0)
    dr = ImageDraw.Draw(im)
    for i0, i1, i2 in tris:
        p0, p1, p2 = pts[i0], pts[i1], pts[i2]
        cx = (p0[0] + p1[0] + p2[0]) / 3.0
        if abs(cx) < 0.195:
            xy = [(p0[3] * 512.0, p0[4] * 512.0), (p1[3] * 512.0, p1[4] * 512.0), (p2[3] * 512.0, p2[4] * 512.0)]
            dr.polygon(xy, fill=255)
    return im.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(1.5))


def recolor_skin_uv(template_im, skin_rgb, hair_rgb, hair_mask=None, mouth_mask=None, is_head=True, hair_shade=0.96):
    im = template_im.copy().convert("RGB")
    w, h = im.size
    px = im.load()
    sr, sg, sb = skin_rgb
    hr, hg, hb = hair_rgb
    hm_px = hair_mask.load() if (is_head and hair_mask is not None) else None
    mm_px = mouth_mask.load() if (is_head and mouth_mask is not None) else None

    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            if mm_px is not None and mm_px[x, y] > 128:
                continue
            luma = (0.299 * r + 0.587 * g + 0.114 * b) / 255.0
            factor = max(0.70, min(1.12, 0.88 + (luma - 0.56) * 0.55))
            skin_px = (int(min(255, sr * factor)), int(min(255, sg * factor)), int(min(255, sb * factor)))
            if hm_px is not None:
                hw = hm_px[x, y] / 255.0
                if hw > 0.01:
                    strand = (0.97 + 0.04 * math.sin(x * 0.72 + y * 0.14)) * hair_shade
                    hair_px = (int(min(255, hr * strand)), int(min(255, hg * strand)), int(min(255, hb * strand)))
                    px[x, y] = (
                        int(hair_px[0] * hw + skin_px[0] * (1.0 - hw)),
                        int(hair_px[1] * hw + skin_px[1] * (1.0 - hw)),
                        int(hair_px[2] * hw + skin_px[2] * (1.0 - hw)),
                    )
                    continue
            px[x, y] = skin_px
    return im


def build_stylized_toon_head_uv(key, spec, clean_modi_head, hair_masks):
    """
    Generate a 100% pure stylized 3D toon AvatarHead UV map (ZERO real photos!).
    Uses modi.glb's neutral smooth Ready Player Me UV base (no pre-baked stubble) + painted toon facial details:
      UV coordinates (flipY=false):
        Mouth center:  (512, 485)
        Nose base:     (512, 560..600)
        Eyes L/R:      (420, 691) & (604, 691)
        Eyebrows:      (415, 725..735) & (609, 725..735)
        Forehead:      (512, 745..800)
        Jaw/chin:      (512, 405..475)
    """
    h_mask_std, h_mask_rec, mouth_mask = hair_masks
    hair_mask = h_mask_rec if key in ("mbapu", "yogi") else h_mask_std

    base_uv = recolor_skin_uv(
        clean_modi_head,
        spec["skin"],
        spec["hair"],
        hair_mask=hair_mask,
        mouth_mask=mouth_mask,
        is_head=True,
        hair_shade=spec.get("hair_shade", 0.96),
    )

    overlay = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    sr, sg, sb = spec["skin"]
    hr, hg, hb = spec["hair"]
    brow_col = (hr, hg, hb, 235)
    lip_col = (int(sr * 0.72), int(sg * 0.48), int(sb * 0.45), 210)
    shade_col = (int(sr * 0.78), int(sg * 0.72), int(sb * 0.68), 95)

    # Soft cheekbone & nose-bridge cartoon sculpt contours
    od.ellipse([496, 565, 528, 695], fill=(int(min(255, sr * 1.10)), int(min(255, sg * 1.08)), int(min(255, sb * 1.06)), 55))
    od.ellipse([362, 540, 442, 650], fill=(shade_col[0], shade_col[1], shade_col[2], 45))
    od.ellipse([582, 540, 662, 650], fill=(shade_col[0], shade_col[1], shade_col[2], 45))

    # Expressive cartoon lips around y=482..502
    if spec["smile"] == "shouting":
        od.ellipse([468, 466, 556, 508], fill=(80, 22, 22, 225))
        od.rectangle([480, 488, 544, 502], fill=(242, 238, 228, 220))
    else:
        od.polygon([(462, 488), (512, 476), (562, 488), (512, 500)], fill=lip_col)
        od.line([(466, 488), (512, 485), (558, 488)], fill=(45, 22, 20, 180), width=4)

    # Eyebrows (remember UV y increases UP toward forehead!)
    if spec["smile"] in ("fierce", "stern", "shouting"):
        od.polygon([(362, 718), (464, 732), (462, 750), (358, 736)], fill=brow_col)
        od.polygon([(662, 718), (560, 732), (562, 750), (666, 736)], fill=brow_col)
    else:
        od.polygon([(360, 728), (415, 744), (464, 736), (460, 722), (412, 728)], fill=brow_col)
        od.polygon([(664, 728), (609, 744), (560, 736), (564, 722), (612, 728)], fill=brow_col)

    # Stylized mustache (above mouth in screen = UV y=506..536)
    m_type = spec.get("mustache", "none")
    if m_type == "trim":
        od.polygon([(466, 514), (512, 524), (558, 514), (554, 502), (512, 510), (470, 502)], fill=(hr, hg, hb, 240))
    elif m_type in ("thick", "salt_pepper"):
        mcol = (95, 95, 102, 235) if m_type == "salt_pepper" else (hr, hg, hb, 245)
        od.polygon([(452, 514), (512, 530), (572, 514), (564, 496), (512, 508), (460, 496)], fill=mcol)
    elif m_type in ("wild", "handlebar"):
        od.polygon([(434, 526), (475, 514), (512, 534), (549, 514), (590, 526), (576, 500), (512, 512), (448, 500)], fill=(hr, hg, hb, 245))
    elif m_type == "bushy_white":
        od.polygon([(452, 516), (512, 532), (572, 516), (566, 498), (512, 510), (458, 498)], fill=(235, 235, 242, 240))
    elif m_type == "white_long":
        od.polygon([(436, 518), (512, 534), (588, 518), (566, 490), (512, 506), (458, 490)], fill=(235, 235, 242, 235))

    # Stylized beard / goatee (below mouth in screen = UV y=402..482)
    b_type = spec.get("beard", "none")
    if b_type == "stubble_goatee":
        od.ellipse([434, 412, 590, 488], fill=(hr, hg, hb, 105))
        od.polygon([(466, 456), (558, 456), (538, 412), (486, 412)], fill=(hr, hg, hb, 210))
    elif b_type in ("full", "salt_pepper"):
        bcol = (105, 105, 112, 215) if b_type == "salt_pepper" else (hr, hg, hb, 230)
        od.polygon([(388, 540), (422, 430), (512, 400), (602, 430), (636, 540), (584, 500), (552, 464), (472, 464), (440, 500)], fill=bcol)
    elif b_type == "trimmed":
        od.ellipse([430, 412, 594, 495], fill=(hr, hg, hb, 200))
    elif b_type == "long_white":
        od.polygon([(422, 470), (602, 470), (555, 396), (469, 396)], fill=(232, 232, 240, 235))

    # Sacred forehead marks (pottu / vibhuti / tilak at y=740..780)
    tlk = spec.get("tilak", "none")
    if tlk == "pottu":
        od.ellipse([499, 750, 525, 776], fill=(185, 20, 28, 250))
    elif tlk == "vibhuti":
        od.rectangle([476, 752, 548, 760], fill=(244, 244, 248, 230))
        od.rectangle([482, 766, 542, 772], fill=(244, 244, 248, 215))
        od.ellipse([503, 742, 521, 760], fill=(196, 28, 28, 240))
    elif tlk == "red_tilak":
        od.rectangle([506, 742, 518, 782], fill=(205, 24, 24, 245))

    # Tapered silver temple streaks for Surya Anna (modi)
    if spec.get("hair_style") == "side_silver":
        od.polygon([(268, 660), (318, 685), (312, 748), (266, 738)], fill=(198, 200, 208, 155))
        od.polygon([(756, 660), (706, 685), (712, 748), (758, 738)], fill=(198, 200, 208, 155))

    overlay = overlay.filter(ImageFilter.GaussianBlur(4.0))
    out = Image.alpha_composite(base_uv.convert("RGBA"), overlay).convert("RGB")
    out.save(os.path.join(FACES_DIR, f"{key}_head_uv.webp"), format="WEBP", quality=92)
    return out


def draw_cartoon_portrait(key, spec, out_path):
    """Render a bold 512x512 cel-shaded comic/cartoon portrait (100% illustration, ZERO real photos)."""
    S = 1024
    c1, c2 = spec["bg"]
    ar, ag, ab = spec["accent"]
    sr, sg, sb = spec["skin"]
    hr, hg, hb = spec["hair"]
    ink = (18, 12, 16)

    im = Image.new("RGB", (S, S), c2)
    dr = ImageDraw.Draw(im)
    for y in range(S):
        t = y / S
        col = (int(c1[0] * (1 - t) + c2[0] * t), int(c1[1] * (1 - t) + c2[1] * t), int(c1[2] * (1 - t) + c2[2] * t))
        dr.line([(0, y), (S, y)], fill=col)

    # Radial spotlight
    dr.ellipse([130, 80, 894, 844], fill=(min(255, c1[0] + 45), min(255, c1[1] + 35), min(255, c1[2] + 35)))

    # Shoulders + outfit + shawl
    top_rgb = spec["top_tint"]
    dr.chord([140, 680, 884, 1340], 180, 360, fill=top_rgb, outline=ink, width=14)
    if spec.get("top_jacket_tint"):
        dr.chord([190, 695, 834, 1340], 180, 360, fill=spec["top_jacket_tint"], outline=ink, width=12)
        dr.polygon([(460, 720), (564, 720), (550, 1024), (474, 1024)], fill=top_rgb, outline=ink)
    if "shawl_colors" in spec:
        sc1, sc2 = spec["shawl_colors"]
        dr.polygon([(220, 720), (350, 700), (390, 1024), (240, 1024)], fill=sc1, outline=ink, width=10)
        dr.polygon([(674, 700), (804, 720), (784, 1024), (634, 1024)], fill=sc2, outline=ink, width=10)
        dr.line([(295, 710), (315, 1024)], fill=(250, 204, 21), width=10)
    elif spec.get("pushpa_floral"):
        for cx, cy in [(310, 860), (440, 910), (620, 880), (720, 840)]:
            dr.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill=(242, 168, 52), outline=(120, 28, 12), width=6)

    # Neck
    neck_sh = (int(sr * 0.78), int(sg * 0.76), int(sb * 0.74))
    dr.rectangle([424, 575, 600, 790], fill=neck_sh, outline=ink, width=12)

    # Ears
    dr.ellipse([264, 415, 340, 545], fill=spec["skin"], outline=ink, width=12)
    dr.ellipse([684, 415, 760, 545], fill=spec["skin"], outline=ink, width=12)

    # Hair back layer
    hs = spec.get("hair_style", "quiff")
    if hs == "bun":
        dr.ellipse([392, 92, 632, 310], fill=(hr, hg, hb), outline=ink, width=14)
        dr.arc([396, 110, 628, 300], 170, 370, fill=(250, 204, 21), width=16)
    elif hs in ("flowing_white", "windswept", "curly_mass"):
        dr.ellipse([240, 150, 784, 535], fill=(hr, hg, hb), outline=ink, width=14)

    # Face silhouette
    dr.ellipse([292, 195, 732, 705], fill=spec["skin"], outline=ink, width=14)

    # Front hair cap
    if hs == "quiff" or hs == "tall_quiff":
        dr.polygon([(292, 390), (288, 225), (420, 130), (640, 115), (748, 220), (732, 385), (675, 290), (490, 270), (345, 300)], fill=(hr, hg, hb), outline=ink, width=12)
    elif hs == "receding_silver" or hs == "flowing_white":
        dr.chord([292, 195, 732, 410], 185, 355, fill=(hr, hg, hb), outline=ink, width=10)
    else:
        dr.chord([286, 175, 738, 450], 175, 365, fill=(hr, hg, hb), outline=ink, width=12)
        if hs == "side_silver":
            dr.polygon([(292, 330), (342, 330), (336, 455), (292, 455)], fill=(205, 210, 218))
            dr.polygon([(682, 330), (732, 330), (732, 455), (688, 455)], fill=(205, 210, 218))

    # Cheekbones highlight
    dr.ellipse([344, 480, 418, 535], fill=(min(255, sr + 18), min(255, sg + 12), min(255, sb + 10)))
    dr.ellipse([606, 480, 680, 535], fill=(min(255, sr + 18), min(255, sg + 12), min(255, sb + 10)))

    # Brows & Eyes
    bcol = (hr, hg, hb)
    dr.line([(356, 395), (464, 385)], fill=bcol, width=22)
    dr.line([(668, 395), (560, 385)], fill=bcol, width=22)
    if spec.get("glasses") == "shades":
        dr.rounded_rectangle([342, 405, 492, 485], radius=18, fill=(14, 14, 22), outline=(250, 204, 21), width=10)
        dr.rounded_rectangle([532, 405, 682, 485], radius=18, fill=(14, 14, 22), outline=(250, 204, 21), width=10)
        dr.line([(492, 430), (532, 430)], fill=(250, 204, 21), width=10)
        dr.line([(360, 422), (430, 468)], fill=(255, 255, 255), width=6)
        dr.line([(550, 422), (620, 468)], fill=(255, 255, 255), width=6)
    else:
        for ex in (418, 606):
            dr.ellipse([ex - 36, 415, ex + 36, 465], fill=(250, 250, 252), outline=ink, width=7)
            dr.ellipse([ex - 16, 421, ex + 16, 459], fill=(34, 22, 18))
            dr.ellipse([ex - 7, 428, ex + 5, 440], fill=(255, 255, 255))
        if spec.get("glasses") in ("rim", "round", "rimless"):
            if spec["glasses"] == "round":
                dr.ellipse([362, 392, 476, 486], outline=(55, 55, 64), width=8)
                dr.ellipse([548, 392, 662, 486], outline=(55, 55, 64), width=8)
            else:
                dr.rounded_rectangle([354, 402, 484, 478], radius=14, outline=(52, 52, 62), width=8)
                dr.rounded_rectangle([540, 402, 670, 478], radius=14, outline=(52, 52, 62), width=8)
            dr.line([(484, 432), (540, 432)], fill=(52, 52, 62), width=7)

    # Stylized nose
    dr.line([(512, 445), (528, 535), (492, 548)], fill=ink, width=10)

    # Tilak / Pottu
    tlk = spec.get("tilak", "none")
    if tlk == "pottu":
        dr.ellipse([496, 326, 528, 358], fill=(195, 20, 28))
    elif tlk == "vibhuti":
        dr.line([(472, 326), (552, 326)], fill=(246, 246, 250), width=10)
        dr.ellipse([500, 336, 524, 360], fill=(195, 28, 28))
    elif tlk == "red_tilak":
        dr.rectangle([504, 314, 520, 366], fill=(210, 24, 24))

    # Mouth + Beard / Mustache
    if spec.get("beard") == "long_white":
        dr.polygon([(345, 555), (679, 555), (595, 860), (429, 860)], fill=(235, 235, 242), outline=ink, width=10)
    elif spec.get("beard") in ("full", "salt_pepper", "trimmed"):
        bcol = (105, 105, 115) if spec["beard"] == "salt_pepper" else (hr, hg, hb)
        dr.chord([294, 455, 730, 725], 0, 180, fill=bcol, outline=ink, width=10)
    elif spec.get("beard") == "stubble_goatee":
        dr.polygon([(448, 600), (576, 600), (548, 700), (476, 700)], fill=(hr, hg, hb), outline=ink, width=8)

    # Mouth
    if spec["smile"] == "shouting":
        dr.ellipse([442, 582, 582, 650], fill=(110, 20, 26), outline=ink, width=10)
        dr.rectangle([460, 588, 564, 608], fill=(246, 244, 238))
    elif spec["smile"] in ("warm", "bold"):
        dr.chord([444, 575, 580, 646], 0, 180, fill=(242, 238, 230), outline=ink, width=10)
    else:
        dr.line([(455, 610), (512, 618), (569, 608)], fill=ink, width=12)

    if spec.get("mustache", "none") != "none":
        mc = (232, 232, 240) if "white" in spec["mustache"] else (hr, hg, hb)
        dr.polygon([(428, 580), (512, 550), (596, 580), (570, 604), (512, 582), (454, 604)], fill=mc, outline=ink, width=8)

    if spec.get("glasses") == "headphones":
        dr.rounded_rectangle([244, 385, 296, 555], radius=24, fill=(34, 211, 238), outline=ink, width=10)
        dr.rounded_rectangle([728, 385, 780, 555], radius=24, fill=(34, 211, 238), outline=ink, width=10)

    # Frame bevel
    dr.rectangle([0, 0, S - 1, S - 1], outline=(ar, ag, ab), width=26)

    im.resize((512, 512), Image.Resampling.LANCZOS).save(out_path, format="WEBP", quality=92)


def draw_gst_maami_cartoons():
    """Generate cartoon Tax Maami portrait + 576x1600 standee cutout (ZERO real photo!)."""
    # 1. Portrait (faces/nirmala.webp)
    maami_spec = {
        "skin": (212, 162, 134),
        "hair": (186, 186, 198),
        "hair_style": "bun",
        "mustache": "none",
        "beard": "none",
        "glasses": "rim",
        "tilak": "pottu",
        "smile": "warm",
        "bg": [(153, 27, 27), (44, 8, 16)],
        "accent": (250, 204, 21),
        "top_tint": (185, 28, 28),
        "shawl_colors": [(250, 204, 21), (185, 28, 28)],
    }
    draw_cartoon_portrait("nirmala", maami_spec, os.path.join(FACES_DIR, "nirmala.webp"))

    # 2. Full standee cutout (576x1600 transparent RGBA WebP for art/nirmala.webp & art/mobile/nirmala.webp)
    W, H = 576, 1600
    stand = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stand)
    ink = (28, 12, 14, 255)
    # Saree body (crimson + gold border)
    sd.polygon([(145, 420), (430, 420), (485, 1495), (90, 1495)], fill=(185, 28, 36, 255), outline=ink, width=10)
    sd.polygon([(130, 430), (310, 420), (460, 1180), (260, 1240)], fill=(250, 204, 21, 255), outline=ink, width=8)
    sd.rectangle([90, 1380, 485, 1495], fill=(250, 204, 21, 255), outline=ink, width=8)
    # Sandals
    sd.ellipse([180, 1495, 275, 1555], fill=(92, 42, 16, 255), outline=ink, width=6)
    sd.ellipse([300, 1495, 395, 1555], fill=(92, 42, 16, 255), outline=ink, width=6)
    # Arms + GST Ledger
    sd.rounded_rectangle([75, 445, 160, 820], radius=36, fill=(212, 162, 134, 255), outline=ink, width=8)
    sd.rounded_rectangle([416, 445, 500, 820], radius=36, fill=(212, 162, 134, 255), outline=ink, width=8)
    sd.rounded_rectangle([140, 680, 436, 980], radius=16, fill=(220, 38, 38, 255), outline=(250, 204, 21, 255), width=10)
    sd.rectangle([168, 725, 408, 795], fill=(250, 204, 21, 255))
    # Head (bun + glasses + pottu + smile)
    sd.rectangle([250, 330, 326, 435], fill=(192, 142, 114, 255), outline=ink, width=8)
    sd.ellipse([235, 92, 341, 198], fill=(165, 165, 178, 255), outline=ink, width=8)
    sd.ellipse([182, 136, 394, 372], fill=(212, 162, 134, 255), outline=ink, width=10)
    sd.chord([182, 128, 394, 256], 180, 360, fill=(186, 186, 198, 255), outline=ink, width=8)
    sd.ellipse([280, 204, 296, 220], fill=(200, 20, 28, 255))
    sd.rounded_rectangle([206, 230, 274, 272], radius=8, fill=(255, 255, 255, 210), outline=(45, 45, 55, 255), width=6)
    sd.rounded_rectangle([302, 230, 370, 272], radius=8, fill=(255, 255, 255, 210), outline=(45, 45, 55, 255), width=6)
    sd.line([(274, 248), (302, 248)], fill=(45, 45, 55, 255), width=5)
    sd.ellipse([234, 242, 248, 258], fill=ink)
    sd.ellipse([328, 242, 342, 258], fill=ink)
    sd.chord([248, 292, 328, 338], 0, 180, fill=(246, 242, 236, 255), outline=ink, width=6)

    stand.save(os.path.join(ART_DIR, "nirmala.webp"), format="WEBP", quality=92)
    stand.save(os.path.join(ART_MOBILE_DIR, "nirmala.webp"), format="WEBP", quality=92)


def tint_fabric_uv(template_im, tint_rgb, size=(512, 512)):
    im = template_im.resize(size, Image.Resampling.LANCZOS).convert("RGB")
    w, h = im.size
    px = im.load()
    samples = []
    for y in range(0, h, 16):
        for x in range(0, w, 16):
            r, g, b = px[x, y]
            samples.append(0.299 * r + 0.587 * g + 0.114 * b)
    med = max(45.0, sorted(samples)[len(samples) // 2])
    tr, tg, tb = tint_rgb
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            lum = 0.299 * r + 0.587 * g + 0.114 * b
            f = max(0.68, min(1.22, lum / med))
            weave = 0.97 + 0.04 * ((x ^ y) & 1)
            px[x, y] = (int(min(255, tr * f * weave)), int(min(255, tg * f * weave)), int(min(255, tb * f * weave)))
    return im


def build_garments_and_body(key, spec, templates, vest_mask):
    body_uv = recolor_skin_uv(templates["AvatarBody"], spec["skin"], spec["hair"], is_head=False)
    body_uv.save(os.path.join(FACES_DIR, f"{key}_body_uv.webp"), format="WEBP", quality=90)

    top_tpl = templates["didi_blouse"] if spec["base"] == "didi" else templates["outfit_top"]
    top_uv = tint_fabric_uv(top_tpl, spec["top_tint"], (512, 512))

    if spec.get("clean_collar"):
        tr, tg, tb = spec["top_tint"]
        tp = top_uv.load()
        for yy in range(512):
            for xx in range(512):
                r, g, b = tp[xx, yy]
                if r + g + b < (tr + tg + tb) * 0.48:
                    tp[xx, yy] = (int(tr * 0.88), int(tg * 0.88), int(tb * 0.88))

    if spec.get("top_jacket_tint"):
        vest_im = tint_fabric_uv(top_tpl, spec["top_jacket_tint"], (512, 512))
        top_uv = Image.composite(vest_im, top_uv, vest_mask)

    if spec.get("pushpa_floral"):
        td = ImageDraw.Draw(top_uv)
        for fy in range(16, 512, 64):
            for fx in range(16, 512, 64):
                td.ellipse([fx - 12, fy - 12, fx + 12, fy + 12], fill=(242, 168, 52))
                td.ellipse([fx - 5, fy - 5, fx + 5, fy + 5], fill=(120, 28, 12))

    top_uv.save(os.path.join(FACES_DIR, f"{key}_top_uv.webp"), format="WEBP", quality=90)

    if spec["base"] == "didi":
        sari_im = templates["didi_sari"].resize((512, 512), Image.Resampling.LANCZOS).convert("RGB")
        px = sari_im.load()
        sr, sg, sb = spec["bottom_tint"]
        br, bg, bb = spec["sari_border"]
        for y in range(512):
            for x in range(512):
                r, g, b = px[x, y]
                f = max(0.70, min(1.18, (0.299 * r + 0.587 * g + 0.114 * b) / 185.0))
                if y >= 412:
                    px[x, y] = (int(min(255, br * f)), int(min(255, bg * f)), int(min(255, bb * f)))
                else:
                    px[x, y] = (int(min(255, sr * f)), int(min(255, sg * f)), int(min(255, sb * f)))
        sari_im.save(os.path.join(FACES_DIR, f"{key}_bottom_uv.webp"), format="WEBP", quality=90)
    else:
        bot_tpl = templates["outfit_dhoti"] if spec.get("bottom_border") else templates["outfit_bottom"]
        bot_uv = tint_fabric_uv(bot_tpl, spec["bottom_tint"], (512, 512))
        if spec.get("bottom_border"):
            bd = ImageDraw.Draw(bot_uv)
            c1, c2 = spec["bottom_border"]
            bd.rectangle([0, 445, 512, 475], fill=c1)
            bd.rectangle([0, 475, 512, 502], fill=c2)
        bot_uv.save(os.path.join(FACES_DIR, f"{key}_bottom_uv.webp"), format="WEBP", quality=90)

    shawl_tpl = templates["outfit_shawl"]
    if "shawl_colors" in spec:
        c1, c2 = spec["shawl_colors"]
        shawl_uv = tint_fabric_uv(shawl_tpl, c1, (256, 256))
        sd = ImageDraw.Draw(shawl_uv)
        sd.rectangle([0, 0, 128, 256], fill=c2)
        sd.rectangle([120, 0, 136, 256], fill=(240, 198, 48))
        shawl_uv.save(os.path.join(FACES_DIR, f"{key}_shawl_uv.webp"), format="WEBP", quality=90)


def remove_legacy_photos():
    removed = 0
    for fn in os.listdir(FACES_DIR):
        if fn.endswith("_face.png") or fn.endswith("_front.webp"):
            os.remove(os.path.join(FACES_DIR, fn))
            removed += 1
    print(f"  Removed {removed} real-photo cache files.")


def main():
    print("1) Removing raw photo files & verifying GLBs...")
    remove_legacy_photos()
    paths = {name: download_glb(name) for name in FIGHTER_IDS + EXTRA_GLBS}

    print("2) Extracting stylized RPM base templates & 3D vertex masks...")
    modi_tex = extract_glb_textures(paths["modi"], {"AvatarHead", "AvatarBody", "outfit_top", "outfit_bottom"})
    rahul_tex = extract_glb_textures(paths["rahul"], {"AvatarHead", "AvatarBody", "outfit_top", "outfit_bottom"})
    didi_tex = extract_glb_textures(paths["didi"], {"AvatarHead", "AvatarBody", "didi_sari", "didi_blouse"})
    yogi_tex = extract_glb_textures(paths["yogi"], {"outfit_dhoti", "outfit_shawl"})

    # Neutral clean RPM base face shading (zero embedded dark stubble)
    clean_modi_head = modi_tex["AvatarHead"]
    base_map = {
        "modi": {**modi_tex, **yogi_tex},
        "rahul": {**rahul_tex, **yogi_tex},
        "didi": {**didi_tex, **yogi_tex},
    }
    hair_masks_map = {b: build_head_3d_masks(b) for b in ("modi", "rahul", "didi")}
    vest_mask = build_vest_uv_mask()

    print("3) Generating stylized 3D toon UVs & cel-shaded 2D cartoon portraits (ZERO real photos)...")
    for key in FIGHTER_IDS:
        spec = FIGHTER_SPECS[key]
        bkey = spec["base"]
        build_stylized_toon_head_uv(key, spec, clean_modi_head, hair_masks_map[bkey])
        build_garments_and_body(key, spec, base_map[bkey], vest_mask)
        draw_cartoon_portrait(key, spec, os.path.join(FACES_DIR, f"{key}.webp"))
        print(f"  OK {key}: built toon head_uv + cartoon portrait")

    draw_gst_maami_cartoons()
    print("  OK nirmala: built cartoon Tax Maami portrait + 576x1600 standee")


if __name__ == "__main__":
    main()
