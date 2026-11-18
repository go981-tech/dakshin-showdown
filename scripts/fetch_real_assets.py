import os
import io
import time
import json
import urllib.request
import urllib.parse
from PIL import Image, ImageEnhance, ImageOps, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC = os.path.join(ROOT, "public")
FACES_DIR = os.path.join(PUBLIC, "faces")
ART_DIR = os.path.join(PUBLIC, "art")
MEMES_DIR = os.path.join(PUBLIC, "assets", "memes")

os.makedirs(FACES_DIR, exist_ok=True)
os.makedirs(os.path.join(ART_DIR, "mobile"), exist_ok=True)
os.makedirs(MEMES_DIR, exist_ok=True)

UA = "DakshinShowdownGame/1.0 (https://localhost:3000; dev@localhost)"
BROWSER_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"

# Face crop parameters: (cx_frac, cy_frac, box_frac) relative to source image min-dim / dimensions
PORTRAIT_SOURCES = {
    "modi":  {"wiki": "M._K._Stalin", "accent": "#e11d48", "crop": (0.50, 0.46, 0.90)},
    "rahul": {"wiki": "Vijay_(actor)", "accent": "#dc2626", "crop": (0.50, 0.36, 0.62)},
    "didi":  {"wiki": "J._Jayalalithaa", "accent": "#16a34a", "crop": (0.50, 0.36, 0.62)},
    "trump": {"wiki": "Allu_Arjun", "accent": "#ea580c", "crop": (0.50, 0.36, 0.60)},
    "yogi":  {"wiki": "Pinarayi_Vijayan", "accent": "#b91c1c", "crop": (0.50, 0.43, 0.88)},
    "nitin": {"wiki": "D._K._Shivakumar", "accent": "#0284c7", "crop": (0.50, 0.38, 0.68)},
    "ravi":  {"wiki": "Pawan_Kalyan", "accent": "#dc2626", "crop": (0.50, 0.36, 0.64)},
    "lalu":  {"wiki": "Seeman_(politician)", "accent": "#eab308", "crop": (0.50, 0.25, 0.48)},
    "mbapu": {"wiki": "Periyar", "accent": "#facc15", "crop": (0.50, 0.44, 0.92)},
    "amit":  {"wiki": "K._Annamalai", "accent": "#f97316", "crop": (0.38, 0.36, 0.72)},
    "dhruv": {"url": "https://yt3.googleusercontent.com/ytc/AIdro_lrMeOj87eBqgzxutjD58IfdwxTzlyfl5JPMd27ga2zeXEi=s900-c-k-c0x00ffffff-no-rj", "accent": "#22d3ee", "crop": (0.50, 0.45, 0.85)},
    "nirmala": {"wiki": "Nirmala_Sitharaman", "accent": "#b91c1c", "crop": (0.50, 0.36, 0.56)},
}

def http_get(url, headers=None, timeout=15):
    req = urllib.request.Request(url, headers=headers or {"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()

def fetch_source_image(spec, key):
    if "wiki" in spec:
        api = f"https://en.wikipedia.org/api/rest_v1/page/summary/{spec['wiki']}"
        summary = json.loads(http_get(api).decode("utf-8"))
        candidates = []
        if summary.get("thumbnail", {}).get("source"):
            candidates.append(summary["thumbnail"]["source"])
        if summary.get("originalimage", {}).get("source"):
            candidates.append(summary["originalimage"]["source"])
        # Prefer thumbnail slightly only if original fails 429, or try thumbnail at higher px first?
        # Try original first, then thumbnail
        ordered = []
        if summary.get("originalimage", {}).get("source"):
            ordered.append(summary["originalimage"]["source"])
        if summary.get("thumbnail", {}).get("source"):
            ordered.append(summary["thumbnail"]["source"])
        for u in ordered:
            try:
                data = http_get(u, {"User-Agent": BROWSER_UA, "Referer": "https://en.wikipedia.org/"})
                return Image.open(io.BytesIO(data)).convert("RGB")
            except Exception as e:
                print(f"  [{key}] retry after {u[:60]}...: {e}")
                time.sleep(0.7)
    if "wiki_ta" in spec:
        try:
            api = f"https://ta.wikipedia.org/api/rest_v1/page/summary/{spec['wiki_ta']}"
            summary = json.loads(http_get(api).decode("utf-8"))
            for kurl in ("thumbnail", "originalimage"):
                u = summary.get(kurl, {}).get("source")
                if u:
                    try:
                        data = http_get(u, {"User-Agent": BROWSER_UA, "Referer": "https://ta.wikipedia.org/"})
                        return Image.open(io.BytesIO(data)).convert("RGB")
                    except Exception:
                        time.sleep(0.5)
        except Exception as e:
            print(f"  [{key}] ta.wiki failed: {e}")
    if "url" in spec or "fallback_wiki" in spec:
        try:
            if "url" in spec:
                data = http_get(spec["url"], {"User-Agent": BROWSER_UA, "Referer": "https://ta.wikipedia.org/"})
                return Image.open(io.BytesIO(data)).convert("RGB")
        except Exception as e:
            print(f"  [{key}] primary URL failed: {e}")
        if "fallback_wiki" in spec:
            api = f"https://en.wikipedia.org/api/rest_v1/page/summary/{spec['fallback_wiki']}"
            summary = json.loads(http_get(api).decode("utf-8"))
            turl = summary["thumbnail"]["source"]
            im = Image.open(io.BytesIO(http_get(turl, {"User-Agent": BROWSER_UA}))).convert("RGB")
            w, h = im.size
            # In C._N._Annadurai_and_E._V._Ramasami_(cropped).JPG, Periyar EVR is standing on the RIGHT (x: 0.48..1.0, y: 0.05..0.52)
            return im.crop((int(w * 0.48), int(h * 0.05), w, int(h * 0.52)))
    raise RuntimeError(f"Could not fetch image for {key}")

SKIN_RGB = {
    "modi": (194, 138, 105),
    "rahul": (210, 152, 112),
    "didi": (196, 141, 114),
    "trump": (195, 136, 114),
    "yogi": (192, 139, 100),
    "nitin": (200, 142, 106),
    "ravi": (192, 139, 100),
    "lalu": (176, 121, 96),
    "mbapu": (185, 135, 106),
    "amit": (192, 139, 100),
    "dhruv": (207, 148, 114),
}

def make_fighter_portraits(key, src_im, spec):
    w, h = src_im.size
    cx_f, cy_f, box_f = spec["crop"]
    side = int(min(w, h) * box_f)
    cx = int(w * cx_f)
    cy = int(h * cy_f)
    x0 = max(0, min(w - side, cx - side // 2))
    y0 = max(0, min(h - side, cy - side // 2))
    face = src_im.crop((x0, y0, x0 + side, y0 + side)).resize((512, 512), Image.Resampling.LANCZOS)
    face = ImageEnhance.Contrast(face).enhance(1.12)
    face = ImageEnhance.Sharpness(face).enhance(1.22)

    # Save feathered & skin-blended 3D face wrap texture at /faces/{key}_face.png
    skin_rgb = SKIN_RGB.get(key, (195, 138, 108))
    skin_bg = Image.new("RGB", (512, 512), skin_rgb)
    inner_mask = Image.new("L", (512, 512), 0)
    ImageDraw.Draw(inner_mask).ellipse([36, 24, 476, 488], fill=255)
    inner_mask = inner_mask.filter(ImageFilter.GaussianBlur(22))
    blended_rgb = Image.composite(face.convert("RGB"), skin_bg, inner_mask)

    outer_alpha = Image.new("L", (512, 512), 0)
    ImageDraw.Draw(outer_alpha).ellipse([8, 6, 504, 506], fill=255)
    outer_alpha = outer_alpha.filter(ImageFilter.GaussianBlur(10))
    face_3d = blended_rgb.convert("RGBA")
    face_3d.putalpha(outer_alpha)
    face_3d.save(os.path.join(FACES_DIR, f"{key}_face.png"), format="PNG")

    # Also save framed UI portrait with subtle accent ring on dark radial card at /faces/{key}.webp
    card = Image.new("RGBA", (512, 512), (24, 14, 10, 255))
    card.paste(face.convert("RGBA"), (0, 0))
    draw = ImageDraw.Draw(card)
    acc = spec["accent"]
    draw.rectangle([4, 4, 507, 507], outline=acc, width=10)
    out_webp = os.path.join(FACES_DIR, f"{key}.webp")
    card.save(out_webp, format="WEBP", quality=90)
    return face

def build_nirmala_art(face_im):
    w, h = 360, 1000
    canvas = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(canvas)

    # Connected neck & Silk Kanchipuram saree silhouette
    d.polygon([(95, 250), (265, 250), (310, 990), (50, 990)], fill=(154, 22, 46, 255))
    d.polygon([(125, 250), (175, 250), (305, 860), (240, 860)], fill=(234, 179, 8, 255))
    d.rectangle([50, 930, 310, 990], fill=(234, 179, 8, 255))
    d.rectangle([55, 945, 305, 975], fill=(127, 29, 29, 255))
    d.ellipse([155, 225, 205, 275], fill=(165, 112, 82, 255))

    # Red Budget / GST Bag + GST 18% ledger ON TOP of saree
    d.rectangle([90, 440, 270, 620], fill=(196, 24, 34, 255), outline=(250, 204, 21, 255), width=6)
    d.rectangle([108, 465, 252, 505], fill=(250, 204, 21, 255))
    d.text((135, 476), "GST 18%", fill=(120, 16, 16, 255))
    d.text((116, 535), "POPCORN TAX!", fill=(255, 250, 235, 255))

    head_sz = 195
    head = face_im.resize((head_sz, head_sz), Image.Resampling.LANCZOS).convert("RGBA")
    mask = Image.new("L", (head_sz, head_sz), 0)
    ImageDraw.Draw(mask).ellipse([6, 6, head_sz - 6, head_sz - 6], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(2))
    canvas.paste(head, (w // 2 - head_sz // 2, 55), mask)

    for p in [os.path.join(ART_DIR, "nirmala.webp"), os.path.join(ART_DIR, "mobile", "nirmala.webp")]:
        canvas.save(p, format="WEBP", quality=90)

# Spoken TTS map -> existing MP3 URLs in main-C7-oASSx.js
TTS_CLIPS = {
    "modi-R8FpxZEb.mp3": ("ta", "உங்களில் ஒருவன்! கலாய்றோம், கிழிக்கிறோம்! இது திராவிட மாடல் ஆட்சி!"),
    "rahul-C7Jjp4hs.mp3": ("ta", "என் நெஞ்சில் குடியிருக்கும் தோழர்களே! வாட் ப்ரோ, இட்ஸ் வெரி ராங் ப்ரோ! ஐ அம் வெயிட்டிங்!"),
    "didi-CjTHLKgc.mp3": ("ta", "மக்களால் நான், மக்களுக்காகவே நான்! நான் நினைத்தால் எதுவும் நடக்கும்!"),
    "trump-Czs6_rQc.mp3": ("te", "పుష్ప అంటే ఫ్లవర్ అనుకున్నావా? ఫైరూ! తగ్గేదే లే! రప రప!"),
    "yogi-CJEN4Csa.mp3": ("ml", "കടക്ക് പുറത്ത്! എൽഡിഎഫ് വരും, എല്ലാം ശരിയാകും! ലാൽ സലാം!"),
    "nitin-B2ZG9HV5.mp3": ("kn", "ನನ್ನ ಹೆಸರು ಡಿ ಕೆ ಶಿವಕುಮಾರ್! ಕನಕಪುರ ಬಂಡೆ! ಆಪರೇಷನ್ ಸಕ್ಸಸ್!"),
    "ravi-BUhOMgaW.mp3": ("te", "సీజ్ ది షిప్! నాకు కొంచెం తిక్క ఉంది, కానీ దానికో లెక్క ఉంది!"),
    "raviwin-Q4j69frZ.mp3": ("te", "చెప్పను బ్రదర్! వంద శాతం స్ట్రైక్ రేట్!"),
    "lalu-vVsgGZuo.mp3": ("ta", "தம்பி! ஆமை கறி சாப்பிட்டியா? ஏகே 47 துப்பாக்கியை பிடிச்சு சுட்டேன்! இது உருட்டு இல்லடா வரலாறு!"),
    "mbapu-D85PVY1T.mp3": ("ta", "வெங்காயம்! பகுத்தறிவு கொண்டு சிந்தி! சுயமரியாதையே மனிதனின் உயிர்!"),
    "mbapuintro-BI_jQwTJ.mp3": ("ta", "நான் சொல்வதை நம்பாதே, உன் அறிவால் சிந்தி!"),
    "gulaam-BnDUPSAr.mp3": ("ta", "பகுத்தறிவு என்றும் தோற்பதில்லை!"),
    "amit-DJ24Mt8b.mp3": ("ta", "நான் சொல்றேன் கேக்குறீங்களா? என்ன சார் இது? எழுதி வச்சுக்கோங்க!"),
    "amitwin-DIIUm105.mp3": ("ta", "என் மண் என் மக்கள்! பிரஸ் மீட் முடிஞ்சது!"),
    "dhruv-CHzIxkIz.mp3": ("ta", "ஹலோ எம்ஜி ஸ்குவேட்! இன்னைக்கு நம்ம எதை பத்தி பார்க்க போறோம்னா, உங்க தோல்வியை பத்திதான்!"),
    "nirmala-Dq7cz8UN.mp3": ("ta", "பாப்கார்னுக்கும் பதினெட்டு சதவீதம் ஜிஎஸ்டி! க்ரீம் பன்னுக்கும் ஜிஎஸ்டி!"),
}

ACTION_MEME_CLIPS = {
    "modi_1": ("ta", "கலாய்றோம், கிழிக்கிறோம்!"),
    "modi_2": ("ta", "உங்களில் ஒருவன்!"),
    "rahul_1": ("ta", "வாட் ப்ரோ, இட்ஸ் வெரி ராங் ப்ரோ!"),
    "rahul_2": ("ta", "ஐ அம் வெயிட்டிங்!"),
    "didi_1": ("ta", "நான் நினைத்தால்!"),
    "didi_2": ("ta", "மக்களால் நான்!"),
    "trump_1": ("te", "తగ్గేదే లే!"),
    "trump_2": ("te", "ఫైర్ హు మైన్!"),
    "yogi_1": ("ml", "കടക്ക് പുറത്ത്!"),
    "yogi_2": ("ml", "ചില്ലുന്ന് ഇരിക്ക്!"),
    "nitin_1": ("kn", "ಕನಕಪುರ ಬಂಡೆ!"),
    "nitin_2": ("kn", "ಆಪರೇಷನ್ ಸಕ್ಸಸ್!"),
    "ravi_1": ("te", "చెప్పను బ్రదర్!"),
    "ravi_2": ("te", "సీజ్ ది షిప్!"),
    "lalu_1": ("ta", "தம்பி, ஆமை கறி சாப்பிட்டியா?"),
    "lalu_2": ("ta", "இது உருட்டு இல்லடா!"),
    "mbapu_1": ("ta", "வெங்காயம்!"),
    "mbapu_2": ("ta", "பகுத்தறிவு!"),
    "amit_1": ("ta", "என்ன சார் இது?!"),
    "amit_2": ("ta", "நான் சொல்றேன் கேக்குறீங்களா?!"),
    "dhruv_1": ("ta", "ஹலோ எம்ஜி ஸ்குவேட்!"),
    "dhruv_2": ("ta", "இன்னைக்கு நம்ம!"),
}

def fetch_tts(lang, text, dest):
    url = "https://translate.googleapis.com/translate_tts?" + urllib.parse.urlencode({
        "ie": "UTF-8",
        "client": "tw-ob",
        "tl": lang,
        "q": text,
    })
    data = http_get(url, {"User-Agent": BROWSER_UA})
    with open(dest, "wb") as f:
        f.write(data)
    return len(data)

print("1) Fetching real portraits...")
for key, spec in PORTRAIT_SOURCES.items():
    im = fetch_source_image(spec, key)
    face = make_fighter_portraits(key, im, spec)
    if key == "nirmala":
        build_nirmala_art(face)
    print(f"  OK {key}: source={im.size}")
    time.sleep(0.55)

print("2) Generating spoken TTS Super & Action clips...")
for fname, (lang, text) in TTS_CLIPS.items():
    dest = os.path.join(PUBLIC, "assets", fname)
    if os.path.exists(dest) and os.path.getsize(dest) > 4000:
        continue
    nbytes = fetch_tts(lang, text, dest)
    print(f"  TTS {fname}: {nbytes} bytes")
    time.sleep(0.18)

for fname, (lang, text) in ACTION_MEME_CLIPS.items():
    dest = os.path.join(MEMES_DIR, f"{fname}.mp3")
    if os.path.exists(dest) and os.path.getsize(dest) > 3000:
        continue
    nbytes = fetch_tts(lang, text, dest)
    print(f"  MEME {fname}.mp3: {nbytes} bytes")
    time.sleep(0.18)

print("Done fetching all real photos and meme voices!")
