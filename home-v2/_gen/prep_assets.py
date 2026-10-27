#!/usr/bin/env python3
"""Prepare the shared image set for both home pages.
Run: /Users/ciaosoft/Claude/BRvault/_System/venv-pw/bin/python prep_assets.py
In : ../src-assets (logos and news thumbnails downloaded from aimesoft.com), approval-block-v2/assets/hero (the approved hero images)
Out: ../assets (what the sites use)"""
import os, shutil
from PIL import Image
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "src-assets")
V2 = os.path.join(os.path.dirname(ROOT), "approval-block-v2", "assets")
OUT = os.path.join(ROOT, "assets")
for d in ("logos", "news", "a", "b", "brand"):
    os.makedirs(os.path.join(OUT, d), exist_ok=True)


def save_jpg(im, path, maxw, q=82):
    im = im.convert("RGB")
    if im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    im.save(path, "JPEG", quality=q, optimize=True, progressive=True)
    print("jpg", os.path.relpath(path, ROOT), im.size, os.path.getsize(path) // 1024, "KB")


def crop(im, box):
    return im.crop(box)


# ---- hero (unchanged from the approved block) + crops that continue the hero's three points
a = Image.open(os.path.join(V2, "hero", "a-scene.jpg")).convert("RGB")
save_jpg(a, os.path.join(OUT, "a", "scene.jpg"), 1600, 82)
# SEE: the eye point of the hero, opened up. HEAR: the mouth point. READ: the card point.
save_jpg(crop(a, (720, 250, 1400, 930)), os.path.join(OUT, "a", "see.jpg"), 900, 84)
save_jpg(crop(a, (730, 540, 1250, 860)), os.path.join(OUT, "a", "hear.jpg"), 900, 84)
save_jpg(crop(a, (360, 690, 900, 1130)), os.path.join(OUT, "a", "read.jpg"), 900, 84)
save_jpg(crop(a, (110, 540, 910, 1200)), os.path.join(OUT, "a", "cta.jpg"), 900, 84)    # card in hand, plant, counter: no face

b = Image.open(os.path.join(V2, "hero", "b-ribbon.jpg")).convert("RGB")
save_jpg(b, os.path.join(OUT, "b", "ribbon.jpg"), 1600, 82)
save_jpg(crop(b, (0, 780, 560, 1290)), os.path.join(OUT, "b", "film.jpg"), 900, 84)
save_jpg(crop(b, (380, 800, 1180, 1290)), os.path.join(OUT, "b", "wave.jpg"), 1000, 84)
save_jpg(crop(b, (1080, 780, 1600, 1290)), os.path.join(OUT, "b", "page.jpg"), 900, 84)
# a deep strip of the ribbon's dark sky for the closing band
save_jpg(crop(b, (0, 0, 1600, 640)), os.path.join(OUT, "b", "sky.jpg"), 1600, 80)

for f in ("logo-blue.png", "logo-white.png"):
    shutil.copy(os.path.join(V2, "brand", f), os.path.join(OUT, "brand", f))

# ---- customer logos: flatten to RGB on white, trim, bring to a common height class
LOGO_MAP = {
    "tokushukai-logo.png": "tokushukai.png", "dentsu-logo.jpg": "dentsu.png", "nexusfrontier_logo_greenblack-02.png": "nexus.png",
    "jcm-logo.jpg": "jcm.png", "tng-logo.png": "tng.png", "rath-logo.png": "rath.png", "9h_official_logo.jpg": "ninehours.png",
    "markitone_logo.png": "markitone.png", "fine_logo_color_002.jpg": "fine.png", "prominent-logo-02_1.png": "prominent.png",
}
for src, dst in LOGO_MAP.items():
    im = Image.open(os.path.join(SRC, "logos", src)).convert("RGBA")
    bg = Image.new("RGBA", im.size, (255, 255, 255, 255)); bg.alpha_composite(im)
    im = bg.convert("RGB")
    arr = np.array(im).astype(int)
    if src.startswith("tokushukai"):                      # the original sits on a light grey plate: lift it to white
        grey = (abs(arr[..., 0] - arr[..., 1]) < 6) & (abs(arr[..., 1] - arr[..., 2]) < 6) & (arr[..., 0] > 225)
        arr[grey] = 255
    nonwhite = (arr.min(axis=2) < 244)
    ys, xs = np.where(nonwhite)
    x0, x1, y0, y1 = max(xs.min() - 2, 0), min(xs.max() + 3, arr.shape[1]), max(ys.min() - 2, 0), min(ys.max() + 3, arr.shape[0])
    im = Image.fromarray(arr.astype("uint8")).crop((x0, y0, x1, y1))
    if im.height > 160:                                   # fine.png is 591 px high
        im = im.resize((round(im.width * 160 / im.height), 160), Image.LANCZOS)
    else:                                                 # small sources: 2x so they hold at 2x screens
        im = im.resize((im.width * 2, im.height * 2), Image.LANCZOS)
    im.save(os.path.join(OUT, "logos", dst), optimize=True)
    print("logo", dst, im.size)

# ---- news thumbnails, 16:10, the originals from the press pages
NEWS = {"cadcam_virtual.png": "dxpo.jpg", "viie_2025.jpg": "viie.jpg", "top10_2025.jpg": "top10.jpg"}
for src, dst in NEWS.items():
    im = Image.open(os.path.join(SRC, "news", src)).convert("RGBA")
    bg = Image.new("RGBA", im.size, (255, 255, 255, 255)); bg.alpha_composite(im); im = bg.convert("RGB")
    w, h = im.size; tw, th = 16, 10
    if w / h > tw / th:
        nw = round(h * tw / th); x0 = 0 if src.startswith("viie") else (w - nw) // 2   # viie: the headline starts at the left edge
        im = im.crop((x0, 0, x0 + nw, h))
    else:
        nh = round(w * th / tw); im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    save_jpg(im, os.path.join(OUT, "news", dst), 960, 82)
