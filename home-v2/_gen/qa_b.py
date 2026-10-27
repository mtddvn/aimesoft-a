#!/usr/bin/env python3
"""Gate for home page B (and reusable for A with SITE_DIR). Per language x width: overflow, contrast on rendered pixels (approved qa.py),
touch targets (<600), text-block overlaps, orphan last lines, images decoded, console errors, outside requests; plus VI glyph coverage.
Run: /Users/ciaosoft/Claude/BRvault/_System/venv-pw/bin/python qa_b.py [site_dir]"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(os.path.dirname(ROOT), "approval-block-v2", "_gen"))
import qa
from playwright.sync_api import sync_playwright

SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "site-b")
HTML = os.path.join(SITE, "index.html")
WIDTHS = [int(x) for x in os.environ.get('QA_WIDTHS', '320,360,390,414,600,768,900,901,1024,1100,1180,1280,1440,1920').split(',')]
THRESH_WORDS = 5

EXTRA = r"""
() => {
  const vis = (e) => { for (let q = e; q && q !== document.documentElement; q = q.parentElement) { const s = getComputedStyle(q); if (s.display === 'none' || s.visibility === 'hidden') return false; } const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0; };
  const out = {orph: [], over: [], imgs: [], sw: document.documentElement.scrollWidth, iw: innerWidth};
  // orphans: last line of a text block with >= 5 words must hold >= 3 words
  const blocks = [...document.querySelectorAll('main p, main h2, main h3, main li, footer p, footer address div, .p-ntitle, .p-ft, .p-iline, .p-cap, .p-lede, .p-desc, .p-line')].filter(e => !e.closest('.stage') && vis(e));
  const seen = new Set();
  for (const e of blocks) {
    if (e.querySelector('p,li,h2,h3') || e.classList.contains('p-frame') || (e.matches('li') && e.closest('.p-news'))) continue;               // only leaf blocks
    const words = []; const w = document.createTreeWalker(e, NodeFilter.SHOW_TEXT); let n;
    while ((n = w.nextNode())) { if (!n.textContent.trim()) continue; if (!vis(n.parentElement)) continue; const re = /\S+/g; let m; const rg = document.createRange();
      while ((m = re.exec(n.textContent))) { rg.setStart(n, m.index); rg.setEnd(n, m.index + m[0].length); const rs = [...rg.getClientRects()].filter(r => r.width > 0); if (rs.length) words.push({t: m[0], top: Math.round(rs[rs.length - 1].top / 4)}); } }
    if (words.length < 5) continue;
    const tops = [...new Set(words.map(x => x.top))].sort((a, b) => a - b);
    if (tops.length < 2) continue;
    const last = words.filter(x => x.top === tops[tops.length - 1]);
    const need = (e.getBoundingClientRect().width < 340 || parseFloat(getComputedStyle(e).fontSize) >= 34) ? 2 : 3; if (last.length < need) out.orph.push({text: words.map(x => x.t).join(' ').slice(0, 60), last: last.map(x => x.t).join(' '), lines: tops.length});
  }
  // overlaps between leaf text elements (not nested), outside the approved hero
  const leaves = [...document.querySelectorAll('main *, footer *')].filter(e => !e.closest('.stage') && vis(e) && getComputedStyle(e).display !== 'inline' && ![...e.childNodes].every(c => c.nodeType !== 3 || !c.textContent.trim()) );
  const R = leaves.map(e => ({e, r: e.getBoundingClientRect()}));
  for (let i = 0; i < R.length; i++) for (let j = i + 1; j < R.length; j++) {
    const a = R[i], b = R[j]; if (a.e.contains(b.e) || b.e.contains(a.e)) continue;
    const ox = Math.min(a.r.right, b.r.right) - Math.max(a.r.left, b.r.left), oy = Math.min(a.r.bottom, b.r.bottom) - Math.max(a.r.top, b.r.top);
    if (ox > 3 && oy > 3) out.over.push((a.e.className || a.e.tagName) + ' x ' + (b.e.className || b.e.tagName) + ' ' + Math.round(ox) + 'x' + Math.round(oy));
  }
  out.over = out.over.slice(0, 6);
  for (const i of document.images) { if (!vis(i)) continue; if (!i.complete || i.naturalWidth === 0) out.imgs.push(i.getAttribute('src')); }
  return out;
}
"""


def extra(html):
    res = {}
    with sync_playwright() as p:
        b = p.chromium.launch()
        for lang in ("en", "vi"):
            for w in WIDTHS:
                mob = w < 600
                ctx = b.new_context(viewport={"width": w, "height": 844 if mob else 900}, device_scale_factor=1, is_mobile=mob, has_touch=mob)
                pg = ctx.new_page(); errs = []; reqs = []
                pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
                pg.on("pageerror", lambda e: errs.append(str(e)))
                pg.on("request", lambda r: reqs.append(r.url) if not r.url.startswith(("file:", "data:")) else None)
                pg.goto("file://%s?lang=%s" % (html, lang), wait_until="load"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(250)
                d = pg.evaluate(EXTRA); d["errs"] = errs; d["reqs"] = reqs
                res[(lang, w)] = d
                ctx.close()
        b.close()
    return res


def main():
    widths = [(w, 1, w < 600) for w in WIDTHS]
    base = qa.run(HTML, widths=widths, langs=("en", "vi"))
    ex = extra(HTML)
    bad = 0
    print("%-4s %-5s %-6s | %s" % ("lang", "w", "H", "findings"))
    for r in base:
        e = ex[(r["lang"], r["w"])]
        f = []
        if r["overflow"] or r["sw"] > r["iw"]: f.append("OVERFLOW %s sw=%s iw=%s" % (r["overflow"][:2], r["sw"], r["iw"]))
        if r["small_fail"]: f.append("CONTRAST<4.5 %s" % r["small_fail"][:3])
        if r["large_fail"]: f.append("LARGE<3 %s" % r["large_fail"][:2])
        tgt = [t for t in r["targets_small"] if not (t["t"] == "" and t["w"] <= 2)]
        if r["w"] < 600 and tgt: f.append("TARGET<44 %s" % tgt[:4])
        if e["orph"]: f.append("ORPHAN %s" % [(o["last"], o["text"][:28]) for o in e["orph"][:3]])
        if e["over"]: f.append("OVERLAP %s" % e["over"][:3])
        if e["imgs"]: f.append("IMG NOT LOADED %s" % e["imgs"][:3])
        if e["errs"]: f.append("CONSOLE %s" % e["errs"][:2])
        if e["reqs"]: f.append("OUTSIDE REQUESTS %s" % e["reqs"][:2])
        bad += bool(f)
        print("%-4s %-5d %-6d | min contrast %s | %s" % (r["lang"], r["w"], r["sh"], r["min_contrast"][0] if r["min_contrast"] else None, "; ".join(f) or "ok"))
    cov = qa.vi_coverage(HTML)
    print("VI glyph coverage (missing chars per family):", cov)
    print("TOTAL rows with findings:", bad, "of", len(base))
    return bad


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
