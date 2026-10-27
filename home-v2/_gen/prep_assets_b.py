#!/usr/bin/env python3
"""Tighter crops of the hero ribbon for the three product columns of page B (different framing from the hero), 5:6.
Run: /Users/ciaosoft/Claude/BRvault/_System/venv-pw/bin/python prep_assets_b.py"""
import os
from PIL import Image, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
src = Image.open(os.path.join(ROOT, "assets", "b", "ribbon.jpg")).convert("RGB")
BOXES = {"see": (50, 820, 450, 1300), "hear": (650, 800, 1050, 1280), "read": (1200, 800, 1600, 1280)}
for k, box in BOXES.items():
    im = src.crop(box).resize((800, 960), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=1.4, percent=55, threshold=2))
    im.save(os.path.join(ROOT, "assets", "b", "t-%s.jpg" % k), "JPEG", quality=84, optimize=True, progressive=True)
    print(k, box)
