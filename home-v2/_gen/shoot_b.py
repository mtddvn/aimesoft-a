#!/usr/bin/env python3
"""Screenshots of site-b: full page and per-section at 1440 and 390, EN and VI. Output ../site-b-shots/
Run: /Users/ciaosoft/Claude/BRvault/_System/venv-pw/bin/python shoot_b.py [sections]"""
import os, sys
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SITE = os.environ.get("SITE_DIR", os.path.join(ROOT, "site-b"))
OUT = os.environ.get("SHOT_DIR", os.path.join(ROOT, "site-b-shots"))
os.makedirs(OUT, exist_ok=True)
SECS = ["products", "multimodal", "industries", "services", "customers", "news", "contact"]
which = sys.argv[1:] or None

with sync_playwright() as p:
    b = p.chromium.launch()
    for lang in ("en", "vi"):
        for w, mob, dpr in ((1440, False, 1), (390, True, 2)):
            ctx = b.new_context(viewport={"width": w, "height": 900 if w > 600 else 844}, device_scale_factor=dpr, is_mobile=mob, has_touch=mob)
            pg = ctx.new_page()
            pg.goto("file://%s/index.html?lang=%s" % (SITE, lang), wait_until="load")
            pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(400)
            tag = "b-%d-%s" % (w, lang)
            if not which or "full" in which:
                pg.screenshot(path=os.path.join(OUT, tag + ".png"), full_page=True)
            for s in SECS + ["hero", "footer"]:
                if which and s not in which: continue
                sel = {"hero": ".stage", "footer": "footer"}.get(s, "#" + s)
                el = pg.query_selector(sel)
                if el: el.screenshot(path=os.path.join(OUT, "%s-%s.png" % (tag, s)))
            ctx.close()
    b.close()
print("shots ->", OUT)
