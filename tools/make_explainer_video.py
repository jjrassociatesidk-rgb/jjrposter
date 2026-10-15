#!/usr/bin/env python3
"""JJR Associates animated explainer (Reel, 1080x1920, 24 fps): an original illustrated
professional presenter (blink, talking mouth, head bob, pointing hand) + animated point cards + captions.
Usage: python3 -I tools/make_explainer_video.py --script tools/video_scripts/tax_audit.json --out videos/x.mp4
Script JSON: {"chip": "...", "scenes": [{"say": "...", "title": "...", "sub": "...", "dur": 4.2}, ...]}
No audio is generated (no TTS in this environment); a silent track is added so Instagram accepts the file."""
import argparse, json, math, os, subprocess, shutil, sys
from multiprocessing import Pool
from PIL import Image, ImageDraw, ImageFont

ap = argparse.ArgumentParser()
ap.add_argument("--script", required=True); ap.add_argument("--out", required=True)
ap.add_argument("--footer", default="assets/footer_card.png"); ap.add_argument("--fps", type=int, default=24)
a = ap.parse_args()
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, "..")
SC = json.load(open(a.script)); scenes = SC["scenes"]
W, H, S, FPS = 1080, 1920, 2, a.fps
navy = (14, 42, 71); orange = (226, 104, 24); green = (34, 139, 76); mute = (96, 112, 134); bg = (246, 248, 252)
skin = (236, 187, 148); skin_d = (214, 160, 122); hair = (36, 30, 34)
IF = "/usr/share/fonts/opentype/inter/"
XB = IF + "InterDisplay-ExtraBold.otf"; BD = IF + "Inter-Bold.otf"; MD = IF + "Inter-Medium.otf"; SB = IF + "Inter-SemiBold.otf"
for p in (XB, BD, MD, SB):
    if not os.path.exists(p): sys.exit("font missing " + p)
F = lambda p, s: ImageFont.truetype(p, int(s * S))
P = lambda v: int(round(v * S))

# timeline
starts = []; t = 0.6
for s in scenes: starts.append(t); t += s["dur"]
TOTAL = t + 0.8
footer = Image.open(os.path.join(ROOT, a.footer)).convert("RGB")
FW, FH = footer.size
ease = lambda x: 1 - (1 - max(0, min(1, x))) ** 3

def wrap(d, text, font, maxw):
    words = text.split(); lines = []; cur = ""
    for w in words:
        c = (cur + " " + w).strip()
        if d.textlength(c, font=font) <= maxw: cur = c
        else: lines.append(cur); cur = w
    lines.append(cur); return lines

def background(img):
    d = ImageDraw.Draw(img)
    d.ellipse((P(600), P(-300), P(1300), P(400)), fill=(222, 232, 246))
    d.ellipse((P(-260), P(1050), P(260), P(1560)), fill=(251, 233, 218))
    for i, c in enumerate((orange, (255, 255, 255), green)):
        d.rectangle((P(360 * i), 0, P(360 * (i + 1)), P(12)), fill=c)

def scene_at(t):
    for i, s in enumerate(scenes):
        if starts[i] <= t < starts[i] + s["dur"]: return i
    return -1

def mouth_env(t, i):
    if i < 0: return 0.0
    st = starts[i]; en = st + scenes[i]["dur"]
    if t < st + 0.15 or t > en - 0.3: return 0.0
    v = abs(math.sin(2 * math.pi * 3.1 * t + 1.3 * math.sin(2 * math.pi * 0.9 * t))) * (0.55 + 0.45 * math.sin(2 * math.pi * 1.7 * t + i))
    return max(0.0, min(1.0, v))

def presenter(img, t, i):
    d = ImageDraw.Draw(img)
    bob = 5 * math.sin(2 * math.pi * 0.55 * t) if i >= 0 else 2 * math.sin(2 * math.pi * 0.4 * t)
    sway = 4 * math.sin(2 * math.pi * 0.35 * t + 1)
    cx = 540 + sway; by = bob
    def E(x0, y0, x1, y1, **k): d.ellipse((P(x0 + 0 * cx), P(y0 + by), P(x1), P(y1 + by)), **k)
    # torso
    body = [(cx - 330, 1420 + by), (cx - 300, 1180 + by), (cx - 210, 1120 + by), (cx + 210, 1120 + by), (cx + 300, 1180 + by), (cx + 330, 1420 + by)]
    d.polygon([(P(x), P(y)) for x, y in body], fill=navy)
    # left arm resting
    d.line([(P(cx - 280), P(1180 + by)), (P(cx - 330), P(1400 + by))], fill=(10, 32, 56), width=P(70))
    # shirt + tie
    d.polygon([(P(cx - 70), P(1118 + by)), (P(cx + 70), P(1118 + by)), (P(cx), P(1250 + by))], fill=(255, 255, 255))
    d.polygon([(P(cx - 18), P(1150 + by)), (P(cx + 18), P(1150 + by)), (P(cx + 26), P(1330 + by)), (P(cx), P(1360 + by)), (P(cx - 26), P(1330 + by))], fill=orange)
    d.polygon([(P(cx - 70), P(1118 + by)), (P(cx - 10), P(1118 + by)), (P(cx - 60), P(1200 + by))], fill=(225, 232, 242))
    d.polygon([(P(cx + 70), P(1118 + by)), (P(cx + 10), P(1118 + by)), (P(cx + 60), P(1200 + by))], fill=(225, 232, 242))
    # neck
    d.rounded_rectangle((P(cx - 42), P(1020 + by), P(cx + 42), P(1140 + by)), radius=P(20), fill=skin_d)
    # right (viewer's right) pointing arm
    talk = i >= 0
    lift = (0.5 + 0.5 * math.sin(2 * math.pi * 0.45 * t)) if talk else 0
    sh = (cx + 255, 1190 + by); el = (cx + 330 + 20 * lift, 1300 - 70 * lift + by); hd = (cx + 300 + 40 * lift, 1130 - 190 * lift + by)
    d.line([(P(sh[0]), P(sh[1])), (P(el[0]), P(el[1]))], fill=navy, width=P(68))
    d.line([(P(el[0]), P(el[1])), (P(hd[0]), P(hd[1]))], fill=navy, width=P(60))
    d.ellipse((P(hd[0] - 34), P(hd[1] - 34), P(hd[0] + 34), P(hd[1] + 34)), fill=skin)
    # head
    hx = cx + 0.6 * sway
    d.ellipse((P(hx - 112), P(768 + by), P(hx + 112), P(1030 + by)), fill=hair)
    d.ellipse((P(hx - 118), P(905 + by), P(hx - 92), P(985 + by)), fill=skin_d)
    d.ellipse((P(hx + 92), P(905 + by), P(hx + 118), P(985 + by)), fill=skin_d)
    d.ellipse((P(hx - 100), P(812 + by), P(hx + 100), P(1050 + by)), fill=skin)
    d.chord((P(hx - 108), P(790 + by), P(hx + 108), P(930 + by)), 180, 360, fill=hair)
    d.polygon([(P(hx - 104), P(880 + by)), (P(hx + 104), P(880 + by)), (P(hx + 100), P(850 + by)), (P(hx - 100), P(850 + by))], fill=hair)
    # eyes
    blink = (t % 3.4) < 0.14
    for ex in (-42, 42):
        x = hx + ex; y = 935 + by
        if blink: d.line([(P(x - 15), P(y)), (P(x + 15), P(y))], fill=hair, width=P(4))
        else:
            d.ellipse((P(x - 15), P(y - 12), P(x + 15), P(y + 12)), fill=(255, 255, 255))
            d.ellipse((P(x - 7 + 3 * math.sin(t)), P(y - 8), P(x + 7 + 3 * math.sin(t)), P(y + 8)), fill=(40, 28, 24))
        d.line([(P(x - 20), P(y - 28 - (3 if i >= 0 else 0))), (P(x + 20), P(y - 30))], fill=hair, width=P(6))
    # glasses
    for ex in (-42, 42):
        d.rounded_rectangle((P(hx + ex - 31), P(902 + by), P(hx + ex + 31), P(965 + by)), radius=P(18), outline=(30, 40, 60), width=P(5))
    d.line([(P(hx - 11), P(930 + by)), (P(hx + 11), P(930 + by))], fill=(30, 40, 60), width=P(5))
    # nose + mouth
    d.arc((P(hx - 12), P(950 + by), P(hx + 12), P(992 + by)), 20, 160, fill=skin_d, width=P(4))
    m = mouth_env(t, i); my = 1010 + by
    if m < 0.08:
        d.arc((P(hx - 30), P(my - 18), P(hx + 30), P(my + 16)), 20, 160, fill=(150, 70, 70), width=P(5))
    else:
        h = 5 + 24 * m
        d.ellipse((P(hx - 26), P(my - h / 2), P(hx + 26), P(my + h / 2 + 4)), fill=(140, 48, 58))
        if h > 14: d.rectangle((P(hx - 18), P(my - h / 2 + 2), P(hx + 18), P(my - h / 2 + 8)), fill=(255, 255, 255))

def panel(img, t, i):
    if i < 0: return
    s = scenes[i]; local = t - starts[i]
    k = ease(local / 0.45); out = 1 - ease((local - (s["dur"] - 0.35)) / 0.3) if local > s["dur"] - 0.35 else 1
    al = max(0, min(1, k * out))
    if al <= 0: return
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    ox = int((1 - k) * 90)
    x0, y0, x1, y1 = 60 + ox, 330, 1020 + ox, 700
    d.rounded_rectangle((P(x0 + 4), P(y0 + 10), P(x1 + 4), P(y1 + 10)), radius=P(36), fill=(14, 42, 71, 40))
    d.rounded_rectangle((P(x0), P(y0), P(x1), P(y1)), radius=P(36), fill=(255, 255, 255, 255))
    d.rounded_rectangle((P(x0), P(y0 + 20), P(x0 + 14), P(y1 - 20)), radius=P(7), fill=orange + (255,))
    d.ellipse((P(x0 + 50), P(y0 + 44), P(x0 + 114), P(y0 + 108)), fill=navy + (255,))
    nf = F(XB, 38); n = str(i + 1); w = d.textlength(n, font=nf)
    d.text((P(x0 + 82) - w / 2, P(y0 + 76)), n, font=nf, fill=(255, 255, 255, 255), anchor="lm")
    tf = F(XB, 62); lines = wrap(d, s["title"], tf, (x1 - x0 - 190) * S)
    for j, ln in enumerate(lines[:2]):
        d.text((P(x0 + 140), P(y0 + 78 + j * 70)), ln, font=tf, fill=navy + (255,), anchor="lm")
    sf = F(MD, 40); ys = y0 + 78 + max(1, len(lines[:2])) * 70 + 34
    for j, ln in enumerate(wrap(d, s.get("sub", ""), sf, (x1 - x0 - 120) * S)[:3]):
        d.text((P(x0 + 60), P(ys + j * 54)), ln, font=sf, fill=(70, 84, 104, 255), anchor="lm")
    if al < 1: layer.putalpha(layer.getchannel("A").point(lambda v: int(v * al)))
    img.alpha_composite(layer)

def caption(img, t, i):
    if i < 0: return
    s = scenes[i]; d = ImageDraw.Draw(img)
    f = F(BD, 42); lines = wrap(d, s["say"], f, 880 * S)[:3]
    lh = 56; hbox = len(lines) * lh + 34; y1 = 1384; y0 = y1 - hbox
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
    ld.rounded_rectangle((P(70), P(y0), P(1010), P(y1)), radius=P(28), fill=(14, 42, 71, 235))
    for j, ln in enumerate(lines):
        ld.text((P(540), P(y0 + 17 + lh / 2 + j * lh)), ln, font=f, fill=(255, 255, 255, 255), anchor="mm")
    img.alpha_composite(layer)

def chip(img):
    d = ImageDraw.Draw(img); f = F(BD, 30); txt = SC.get("chip", "EXPLAINER")
    w = d.textlength(txt, font=f) / S + 70
    d.rounded_rectangle((P(540 - w / 2), P(232), P(540 + w / 2), P(292)), radius=P(30), fill=navy)
    d.text((P(540), P(262)), txt, font=f, fill=(255, 255, 255), anchor="mm")

def progress(img, t):
    d = ImageDraw.Draw(img); x = 80 + (920 * min(1, t / TOTAL))
    d.rounded_rectangle((P(80), P(1800 + 0), P(1000), P(1806)), radius=P(3), fill=(222, 229, 239))
    d.rounded_rectangle((P(80), P(1800), P(x), P(1806)), radius=P(3), fill=orange)

fcard = footer.resize((P(FW), P(FH)), Image.LANCZOS)
fmask = Image.new("L", fcard.size, 0); ImageDraw.Draw(fmask).rounded_rectangle((0, 0, fcard.size[0] - 1, fcard.size[1] - 1), radius=P(28), fill=255)

def render(n):
    t = n / FPS; i = scene_at(t)
    img = Image.new("RGBA", (W * S, H * S), bg + (255,)); background(img)
    chip(img); presenter(img, t, i); panel(img, t, i); caption(img, t, i)
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((P(50), P(1394 + 8), P(1030), P(1768 + 8)), radius=P(28), fill=(14, 42, 71, 40)); img.alpha_composite(sh)
    img.paste(fcard, (P(50), P(1394)), fmask); progress(img, t)
    img.convert("RGB").resize((W, H), Image.LANCZOS).save(os.path.join(TMP, "f%05d.png" % n))

if __name__ == "__main__":
    TMP = os.path.join(os.path.dirname(os.path.abspath(a.out)), "_frames"); shutil.rmtree(TMP, ignore_errors=True); os.makedirs(TMP)
    N = int(TOTAL * FPS)
    import multiprocessing as mp
    with mp.get_context("fork").Pool(min(8, os.cpu_count() or 2)) as pool: pool.map(render, range(N), chunksize=6)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(TMP, "f%05d.png"),
                    "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100", "-shortest",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-r", str(FPS), "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", a.out], check=True)
    shutil.rmtree(TMP, ignore_errors=True)
    print("saved", a.out, "%.1fs" % TOTAL)
