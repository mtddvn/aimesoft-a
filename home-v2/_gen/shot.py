#!/usr/bin/env python3
"""shot.py <site-dir> <prefix> [--sections]  : full-page PNGs at 1440 and 390, EN and VI (+ per-section crops with --sections).
Run: /Users/ciaosoft/Claude/BRvault/_System/venv-pw/bin/python shot.py /abs/site-a a"""
import os, sys
from playwright.sync_api import sync_playwright

site, prefix = sys.argv[1], sys.argv[2]
sections = "--sections" in sys.argv
out = os.path.join(os.path.dirname(site), "shots-" + prefix)
os.makedirs(out, exist_ok=True)
url0 = "file://" + os.path.join(site, "index.html")
with sync_playwright() as p:
    b = p.chromium.launch()
    for w, h, mobile in ((1440, 900, False), (390, 844, True)):
        for lang in ("en", "vi"):
            ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=1, is_mobile=mobile, has_touch=mobile)
            pg = ctx.new_page()
            errs = []
            pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.goto(url0 + "?lang=" + lang)
            pg.wait_for_load_state("networkidle")
            # lazy images: scroll through once
            H = pg.evaluate("document.documentElement.scrollHeight")
            for y in range(0, H, 600):
                pg.evaluate("window.scrollTo(0,%d)" % y); pg.wait_for_timeout(40)
            pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(300)
            pg.screenshot(path=os.path.join(out, "%s-%d-%s.png" % (prefix, w, lang)), full_page=True)
            if sections:
                for sid in pg.evaluate("[...document.querySelectorAll('main > section[id], footer')].map(e=>e.id||e.tagName)"):
                    el = pg.query_selector("#" + sid) if sid != "FOOTER" else pg.query_selector("footer")
                    if el: el.screenshot(path=os.path.join(out, "%s-%d-%s-%s.png" % (prefix, w, lang, sid.lower())))
            print(w, lang, "H", pg.evaluate("document.documentElement.scrollHeight"), "errors", errs[:3])
            ctx.close()
    b.close()
