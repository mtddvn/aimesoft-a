#!/usr/bin/env python3
"""qa_full.py <site-dir> [--fast]  Full-page gate for a built home page (generic: works for site-a and site-b).
Per (lang x width): horizontal overflow (incl. elements that poke out of the page), images loaded, console errors, external requests,
orphans (last line < 3 words in blocks of >= 5 words, headings included), touch targets (< 600 px, buttons and standalone links), anchors resolve, h1 count, img alt.
Text contrast measured on PIXELS: render once with all text transparent, sample the area behind every text line, worst case vs the text colour.
Run: /Users/ciaosoft/Claude/BRvault/_System/venv-pw/bin/python qa_full.py /abs/site-a"""
import io, json, os, re, sys
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright

SITE = sys.argv[1]
FAST = "--fast" in sys.argv
URL = "file://" + os.path.join(SITE, "index.html")
WIDTHS = [320, 360, 390, 414, 600, 768, 900, 901, 1024, 1100, 1180, 1280, 1440, 1920]
CONTRAST_WIDTHS = {390, 768, 1440}

JS = r"""
(W) => {
  const vis = (e) => { const s = getComputedStyle(e), r = e.getBoundingClientRect(); return s.display!=='none' && s.visibility!=='hidden' && r.width>0 && r.height>0 && parseFloat(s.opacity)>0.01; };
  const anyHidden = (e) => { let q = e; while (q && q !== document.documentElement) { if (!vis(q)) return true; q = q.parentElement; } return false; };
  const out = {iw: W, sw: document.documentElement.scrollWidth, sh: document.documentElement.scrollHeight};
  // overflow: visible elements poking beyond the viewport, not clipped by an ancestor that itself fits
  const bad = [];
  for (const e of document.body.querySelectorAll('*')) {
    if (anyHidden(e)) continue; const r = e.getBoundingClientRect();
    if (r.right > W + 0.5 || r.left < -0.5) {
      let clipped = false, p = e.parentElement;
      while (p && p !== document.body) { const o = getComputedStyle(p); if (o.overflowX !== 'visible') { const pr = p.getBoundingClientRect(); if (pr.right <= W + 0.5 && pr.left >= -0.5) { clipped = true; break; } } p = p.parentElement; }
      if (!clipped) bad.push((e.className||e.tagName).toString().slice(0,28) + ' ' + Math.round(r.left) + '..' + Math.round(r.right));
    }
  }
  out.overflow = bad.slice(0, 6);
  // text lines + orphans
  const lines = [], orph = [];
  const tw = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n;
  while ((n = tw.nextNode())) {
    const t = n.textContent.trim(); if (!t) continue; const el = n.parentElement;
    if (['SCRIPT','STYLE','NOSCRIPT'].includes(el.tagName) || anyHidden(el)) continue;
    const range = document.createRange(); range.selectNodeContents(n);
    const rects = [...range.getClientRects()].filter(r => r.width > 1 && r.height > 1);
    if (!rects.length) continue;
    const s = getComputedStyle(el);
    const tops = {}; for (const r of rects) { const k = Math.round(r.top / 3); (tops[k] = tops[k] || []).push(r); }
    const ls = Object.values(tops).map(g => ({x: Math.min(...g.map(r => r.left)) + scrollX, y: Math.min(...g.map(r => r.top)) + scrollY, r: Math.max(...g.map(r => r.right)) + scrollX, b: Math.max(...g.map(r => r.bottom)) + scrollY}));
    lines.push({text: t.slice(0, 40), cls: (el.closest('[class]')?.className || '').toString().slice(0, 26), color: s.color, size: parseFloat(s.fontSize), weight: parseInt(s.fontWeight), lines: ls});
  }
  out.lines = lines;
  // orphan check on whole blocks
  for (const b of document.querySelectorAll('p, h1, h2, h3, li, .p-lede, .sub')) {
    if (anyHidden(b)) continue;
    if (b.querySelector('p, li, h1, h2, h3') ) continue;
    const words = []; const w = document.createTreeWalker(b, NodeFilter.SHOW_TEXT); let m; const range = document.createRange();
    while ((m = w.nextNode())) { if (anyHidden(m.parentElement)) continue; const re = /\S+/g; let mm; while ((mm = re.exec(m.textContent))) { range.setStart(m, mm.index); range.setEnd(m, mm.index + mm[0].length); const r = range.getClientRects()[0]; if (r && r.width > 0) words.push({w: mm[0], top: Math.round(r.top / 4)}); } }
    if (words.length < 5) continue;
    const by = {}; words.forEach(x => (by[x.top] = by[x.top] || []).push(x.w)); const ks = Object.keys(by).map(Number).sort((a, b) => a - b);
    if (ks.length < 2) continue; const last = by[ks[ks.length - 1]];
    const bw = b.getBoundingClientRect().width; const need = bw < 420 ? 2 : 3;
    if (last.length < need) orph.push((b.className || b.tagName) + ': ' + last.join(' ') + ' | ' + words.length + 'w/' + ks.length + 'L');
  }
  out.orphans = orph.slice(0, 12);
  // touch targets
  out.targets = [...document.querySelectorAll('a[href], button')].filter(e => !anyHidden(e)).map(e => { const r = e.getBoundingClientRect(); const inPara = e.closest('p') && e.closest('p').textContent.trim() !== e.textContent.trim(); return {t: (e.innerText || e.getAttribute('aria-label') || '').trim().slice(0, 22), w: Math.round(r.width), h: Math.round(r.height), inPara}; });
  // images
  out.imgs = [...document.images].filter(i => !anyHidden(i)).map(i => ({src: (i.getAttribute('src') || '').slice(-40), ok: i.complete && i.naturalWidth > 0, alt: i.getAttribute('alt')}));
  out.h1 = document.querySelectorAll('h1').length;
  out.h2 = [...document.querySelectorAll('h2')].filter(e => !anyHidden(e)).length;
  out.anchors = [...document.querySelectorAll('a[href^="#"]')].map(a => a.getAttribute('href')).filter(h => h.length > 1 && !document.querySelector(h));
  out.ids = (() => { const c = {}; document.querySelectorAll('[id]').forEach(e => c[e.id] = (c[e.id] || 0) + 1); return Object.entries(c).filter(([k, v]) => v > 1).map(([k]) => k); })();
  return out;
}
"""


def lum(c):
    c = np.asarray(c, dtype=float) / 255.0
    c = np.where(c <= 0.03928, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


def parse(col):
    m = re.findall(r"[\d.]+", col)
    v = [float(x) for x in m]
    return v[:3], (v[3] if len(v) > 3 else 1.0)


def contrast_fail(lines, shot):
    arr = np.array(shot.convert("RGB")); H, W = arr.shape[:2]
    small, large, worst = [], [], 99
    for L in lines:
        fg, a = parse(L["color"])
        if a < 0.05: continue
        isl = L["size"] >= 24 or (L["size"] >= 18.66 and L["weight"] >= 700)
        for ln in L["lines"]:
            x0, x1, y0, y1 = int(max(ln["x"], 0)), int(min(ln["r"], W)), int(max(ln["y"], 0)), int(min(ln["b"], H))
            if x1 - x0 < 2 or y1 - y0 < 2: continue
            reg = arr[y0:y1, x0:x1].reshape(-1, 3).astype(float)
            # blend text alpha over the background pixels
            fgb = np.array(fg)[None, :] * a + reg * (1 - a)
            lf, lb = lum(fgb), lum(reg)
            ratio = (np.maximum(lf, lb) + 0.05) / (np.minimum(lf, lb) + 0.05)
            r = float(np.percentile(ratio, 3))
            worst = min(worst, r)
            if r < (3.0 if isl else 4.5):
                (large if isl else small).append("%s|%s %.2f" % (L["cls"], L["text"][:24], r))
    return small, large, worst


def main():
    bad_total = 0
    with sync_playwright() as p:
        b = p.chromium.launch()
        widths = [390, 1440] if FAST else WIDTHS
        for lang in ("en", "vi"):
            for w in widths:
                mobile = w < 600
                ctx = b.new_context(viewport={"width": w, "height": 900}, device_scale_factor=1, is_mobile=mobile, has_touch=mobile)
                pg = ctx.new_page(); errs = []; ext = []
                pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
                pg.on("pageerror", lambda e: errs.append(str(e)))
                pg.on("request", lambda r: ext.append(r.url) if not r.url.startswith(("file:", "data:")) else None)
                pg.goto(URL + "?lang=" + lang); pg.wait_for_load_state("networkidle")
                H = pg.evaluate("document.documentElement.scrollHeight")
                for y in range(0, H, 500):
                    pg.evaluate("window.scrollTo(0,%d)" % y); pg.wait_for_timeout(30)
                pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(250)
                r = pg.evaluate(JS, w)
                flags = []
                if r["sw"] > r["iw"]: flags.append("SCROLLW %d>%d" % (r["sw"], r["iw"]))
                if r["overflow"]: flags.append("OVERFLOW %s" % r["overflow"][:3])
                if r["orphans"]: flags.append("ORPHAN %s" % r["orphans"][:4])
                badi = [i for i in r["imgs"] if not i["ok"]]
                if badi: flags.append("IMG %s" % badi[:3])
                if any(i["alt"] is None for i in r["imgs"]): flags.append("ALT-MISSING")
                if errs: flags.append("ERR %s" % errs[:2])
                if ext: flags.append("EXT %s" % ext[:2])
                if r["h1"] != 1: flags.append("H1x%d" % r["h1"])
                if r["anchors"]: flags.append("ANCHOR %s" % r["anchors"])
                if r["ids"]: flags.append("DUPID %s" % r["ids"])
                if w < 600:
                    ts = [t for t in r["targets"] if (t["h"] < 44 or t["w"] < 44) and not t["inPara"]]
                    if ts: flags.append("TARGET<44 %s" % [(t["t"], t["w"], t["h"]) for t in ts[:4]])
                cinfo = ""
                if w in CONTRAST_WIDTHS:
                    pg.add_style_tag(content="*{color:transparent!important;text-shadow:none!important;-webkit-text-fill-color:transparent!important;caret-color:transparent!important}")
                    pg.wait_for_timeout(150)
                    shot = Image.open(io.BytesIO(pg.screenshot(full_page=True)))
                    small, large, worst = contrast_fail(r["lines"], shot)
                    cinfo = "minC %.2f" % worst
                    if small: flags.append("SMALL<4.5 %s" % small[:4])
                    if large: flags.append("LARGE<3 %s" % large[:4])
                bad_total += len(flags)
                print(lang, w, "H", r["sh"], cinfo, "|", " ; ".join(flags) or "ok")
                ctx.close()
        b.close()
    print("FLAGGED WIDTH-LANG CASES:", bad_total)


main()
