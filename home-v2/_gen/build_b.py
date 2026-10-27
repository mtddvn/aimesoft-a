#!/usr/bin/env python3
"""Aimesoft 2.0 home page B (dark) - generator, v0.2.0. Reads content.py + b.page.tpl.html + the shared assets, writes ../site-b/ (GitHub Pages ready).
Run: /Users/ciaosoft/Claude/BRvault/_System/venv-pw/bin/python build_b.py
Gates inside: no selector declared twice, new classes carry the p- prefix, no internal words, no forbidden characters, every local asset exists,
no comments left in the written file."""
import html as H
import importlib.util, json, math, os, random, re, shutil, sys
from PIL import Image
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
APPROVED = os.path.join(os.path.dirname(ROOT), "approval-block-v2")
OUT = os.environ.get("BUILD_OUT", os.path.join(ROOT, "site-b"))
ASSETS = os.path.join(ROOT, "assets")
DOMAIN = "aimesoft-b.ciaosoft.vn"
VERSION = "0.2.0"

spec = importlib.util.spec_from_file_location("content", os.path.join(HERE, "content.py"))
C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
CFG = json.load(open(os.path.join(APPROVED, "_gen", "cfg.json")))["b"]


def esc(s):
    return H.escape(s, quote=False)


# ---- text: Vietnamese compounds, hyphen tokens, short parentheses and the last words of a block stay on one line (ca 13, 22, 94)
VI_COMP = ["nền tảng", "toàn cầu", "hệ thống", "đa thể thức", "thị giác", "tiếng nói", "ngôn ngữ", "trí tuệ nhân tạo", "khách hàng", "sản phẩm",
           "dịch vụ", "tin tức", "liên hệ", "tư vấn", "khám phá", "nhận diện", "khuôn mặt", "tổng hợp", "mô hình", "nhận dạng", "kết hợp", "triển khai",
           "trên toàn cầu", "hơn 200 lượt triển khai", "lượt triển khai", "một nền tảng", "đã triển khai",
           "chăm sóc khách hàng", "chăm sóc sức khỏe", "tài chính", "ngân hàng", "giáo dục", "du lịch", "thương mại điện tử", "pháp luật", "bán lẻ",
           "khách sạn", "y tế", "bệnh án", "cửa hàng", "siêu thị", "hình ảnh", "văn bản", "giọng nói", "người nói", "chữ in", "độ chính xác",
           "lễ tân", "ứng dụng", "doanh nghiệp", "bản đồ", "danh hiệu", "triển lãm", "đổi mới sáng tạo", "quốc tế", "thuyết trình", "đánh giá", "hỗ trợ",
           "khai phá", "thấu hiểu", "lời khuyên", "giải pháp", "phân tích", "thông minh", "dữ liệu", "ngành công nghiệp", "cao hơn", "chúng tôi",
           "chứng minh thư", "hộ chiếu", "bằng lái xe", "số hoá", "chữ viết", "nhận biết", "tuân theo", "hướng dẫn", "chỉ dẫn", "máy chủ", "tiếng Nhật", "tiếng Việt",
           "Hà Nội", "Cầu Giấy", "Thủ Đức", "TP. Hồ Chí Minh", "Hồ Chí Minh", "Mai Chí Thọ", "Duy Tân", "Việt Á Tower", "An Phú", "Miền Nam"]
EN_KEEP = ["200+ installations", "Top 10", "High Performance", "San Jose", "Mai Chi Tho", "Thu Duc City", "An Phu Ward", "Cau Giay", "Duy Tan Street", "Viet A Tower",
           "Minato-ku", "Southern Vietnam", "HCMC, Vietnam", "Hanoi, Vietnam", "Tokyo 105-0022, Japan", "California 95131, USA"]
HYPHEN = r"[\w]+(?:-[\w]+)+"


def _nw(s):
    return '<span class="nb">%s</span>' % s


def fmt(text, lang, bind=0):
    """Escape and protect line breaks. bind = number of last words that must stay together (0 = none)."""
    words = text.split(" ")
    head, tail = text, ""
    if bind and len(words) >= bind + 3:
        head, tail = " ".join(words[:-bind]), " ".join(words[-bind:])
    pats = sorted(set(VI_COMP + EN_KEEP if lang == "vi" else EN_KEEP), key=len, reverse=True)
    out = esc(head)
    out = re.sub(r"(?<![\w-])((?:%s)|(?:%s)|(?:\([^()]{1,17}\)))(?![\w-])" % ("|".join(re.escape(esc(p)) for p in pats), HYPHEN), lambda m: _nw(m.group(1)), out, flags=re.I) if head else out
    if tail:
        out = out + " " + _nw(esc(tail))
    return out


def T(en, vi=None, bind=0):
    """EN/VI pair. vi=None or equal: one string for both languages (the VI site keeps it in English)."""
    if vi is None or vi == en:
        return fmt(en, "en", bind)
    return '<span class="en">%s</span><span class="vi">%s</span>' % (fmt(en, "en", bind), fmt(vi, "vi", bind))


ARROW = '<svg class="p-arrow" width="22" height="10" viewBox="0 0 22 10" aria-hidden="true"><path d="M0 5H20M16 1l4 4-4 4" fill="none" stroke="currentColor" stroke-width="1.3"/></svg>'


def A(urls, inner, cls="", blank=True, extra=""):
    en, vi = urls
    t = ' target="_blank" rel="noopener"' if blank else ""
    return '<a%s href="%s" data-en="%s" data-vi="%s"%s%s>%s</a>' % (' class="%s"' % cls if cls else "", en, en, vi, t, extra, inner)


def dia():
    return '<i class="dia"></i>'


def nb(h):
    """Vietnamese compounds in the simple VI spans of the approved hero (same pass as the approved block); sections do their own in T()."""
    def vi(m):
        t = m.group(2)
        for w in sorted(set(VI_COMP), key=len, reverse=True):
            t = re.sub(r"(?i)(?<![\w>])(%s)(?![\w<])" % re.escape(w), lambda k: _nw(k.group(1)), t)
        return m.group(1) + t + m.group(3)
    return re.sub(r'(<span class="vi">)([^<]*)(</span>)', vi, h)


# ---- colours: the page background is the flat indigo at the top of the hero ribbon (as in the approved block)
def hero_bg():
    im = np.array(Image.open(os.path.join(ASSETS, "b", "ribbon.jpg")).convert("RGB")).astype(float)
    h, w = im.shape[:2]
    c = np.median(im[: h // 12, : w // 3].reshape(-1, 3), axis=0).round().astype(int)
    return "#%02X%02X%02X" % tuple(c), c


# ---- sections
def head(label, h2, lede=None, hid="", bind_lede=3):
    return ('<div class="p-head"><p class="p-eye">%s%s</p><div class="p-hbody"><h2 class="p-h2" id="%s">%s</h2>%s</div></div>'
            % (dia(), label, hid, h2, ('<p class="p-lede">%s</p>' % lede) if lede else ""))


AIMENICORN = ("Aimenicorn is a Multimodal AI ecosystem developed by Aimesoft to simplify the process of applying Multimodal AI technologies in various industries.",
              "Aimenicorn là một hệ sinh thái trí tuệ nhân tạo đa thể thức được phát triển bởi Aimesoft.")
VIEW_ALL = ("View all", "Xem tất cả")
READ_MORE = ("Read more", "Chi tiết")
SEE_SERVICES = ("Read more", "Xem thêm")
CLAIM = "The FIRST Company to Develop Multimodal AI with 200+ Installations Worldwide"

# purely geometric overlays, one per sense (viewBox = the 400 x 480 crop; no numbers, no words)
_TICKS = "".join("M%d %dV%d" % (x, 400, 400 + (14 if (x // 16) % 5 == 0 else 7)) for x in range(8, 400, 16))
OV = {
    "see": ('<svg class="p-ov" viewBox="0 0 400 480" preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">'
            '<g fill="none" stroke="currentColor" stroke-width="1.4" vector-effect="non-scaling-stroke">'
            '<path d="M96 150V126H120M280 126H304V150M304 300V324H280M120 324H96V300" vector-effect="non-scaling-stroke"/>'
            '<path d="M24 226H376" stroke-dasharray="2 5" vector-effect="non-scaling-stroke"/>'
            '<path d="M24 218V234M376 218V234" vector-effect="non-scaling-stroke"/></g></svg>'),
    "hear": ('<svg class="p-ov" viewBox="0 0 400 480" preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">'
             '<g fill="none" stroke="currentColor" stroke-width="1.4" vector-effect="non-scaling-stroke">'
             '<path d="M176 56V424" vector-effect="non-scaling-stroke"/>'
             '<path d="M170 56L176 49L182 56L176 63Z" fill="currentColor" vector-effect="non-scaling-stroke"/>'
             '<path d="%s" stroke-opacity=".8" vector-effect="non-scaling-stroke"/></g></svg>' % _TICKS),
    "read": ('<svg class="p-ov p-ov-ink" viewBox="0 0 400 480" preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">'
             '<g fill="none" stroke="currentColor" stroke-width="1.5" vector-effect="non-scaling-stroke">'
             '<path d="M236 128V108H256M356 108H376V128M376 214V234H356M256 234H236V214" vector-effect="non-scaling-stroke"/>'
             '<path d="M246 142H366M246 168H352M246 194H360" stroke-opacity=".38" vector-effect="non-scaling-stroke"/></g></svg>'),
}


def sec_products():
    P = {p["key"]: p for p in C.PRODUCTS}
    imgs = {"face": ("assets/b/t-see.jpg", "see", "Frames of 35mm film on the ribbon.", "Các khung phim 35mm trên dải băng."),
            "speech": ("assets/b/t-hear.jpg", "hear", "A waveform printed on the ribbon.", "Dạng sóng âm in trên dải băng."),
            "card": ("assets/b/t-read.jpg", "read", "A printed page curling at the end of the ribbon.", "Trang giấy in cuộn ở cuối dải băng.")}

    def feat(p):
        return '<ul class="p-feat">%s</ul>' % "".join("<li>%s</li>" % T(*c) for c in p["chips"])

    def entry(p):
        src, ov, aen, avi = imgs[p["key"]]
        h = ('<div class="p-entry"><figure class="p-fig"><img src="%s" width="800" height="960" alt="" data-alt-en="%s" data-alt-vi="%s">%s</figure>'
             % (src, aen, avi, OV[ov]))
        h += '<h3 class="p-name">%s</h3><p class="p-line">%s</p><p class="p-desc">%s</p>%s' % (p["name"], T(*p["line"]), T(*p["desc"], bind=3), feat(p))
        h += A(p["url"], '<span>%s</span>%s' % (T(*C.LEARN), ARROW), "p-more")
        return h + "</div>"

    cols = []
    for i, key in enumerate(("face", "speech", "card")):
        p = P[key]
        cols.append('<article class="p-col"><header class="p-colhead"><span class="p-n">0%d</span><span class="p-v">%s</span></header>%s</article>' % (i + 1, T(*p["verb"]), entry(p)))
    g = P["gpt"]
    gpt = ('<article class="p-gpt"><header class="p-colhead"><span class="p-n">04</span><span class="p-v">%s</span>%s</header>'
           '<div class="p-gptgrid"><div><h3 class="p-name p-gptname">%s</h3><p class="p-line">%s</p></div><p class="p-desc">%s</p>'
           '<div class="p-gptcol">%s%s</div></div></article>'
           % (T(*g["verb"]), A(C.PRODUCTS_ALL, '<span>%s</span>%s' % (T(*VIEW_ALL), ARROW), "p-more p-all"), g["name"], T(*g["line"]), T(*g["desc"], bind=3), feat(g),
              A(g["url"], '<span>%s</span>%s' % (T(*C.LEARN), ARROW), "p-more")))
    dots = '<div class="p-dots" aria-hidden="true"><i class="p-on"></i><i></i><i></i></div>'
    return ('<section class="p-sec" id="products" aria-labelledby="p-h-products"><div class="p-wrap">%s'
            '<div class="p-cols" tabindex="0" role="group" aria-label="Products" data-aria-en="Products" data-aria-vi="Sản phẩm">%s</div>%s%s</div></section>'
            % (head(T("Aimenicorn ecosystem", "Hệ sinh thái Aimenicorn"), T("Our products", "Sản phẩm"), T(*AIMENICORN, bind=3), hid="p-h-products"), "".join(cols), dots, gpt))


def sec_numbers():
    n0 = C.NUMBERS[0]
    lead = '<div class="p-lead-n"><p class="p-big">%s</p><p class="p-bigcap">%s</p></div>' % (n0[0], T(n0[1], n0[2]))
    four = "".join('<div class="p-fig-n"><p class="p-num">%s</p><p class="p-cap">%s</p></div>' % (n[0], T(n[1], n[2], bind=2)) for n in C.NUMBERS[1:])
    h = head(T("Aimesoft"), T("Multimodal AI"), T(C.MM_EN, C.MM_VI, bind=3), hid="p-h-mm")
    return '<section class="p-sec" id="multimodal" aria-labelledby="p-h-mm"><div class="p-wrap">%s<div class="p-nums">%s<div class="p-four">%s</div></div></div></section>' % (h, lead, four)


def sec_industries():
    rows = []
    for ind in C.INDUSTRIES:
        links = "".join(A(u, '<span>%s</span>%s' % (esc(n), ARROW), "p-pill") for n, u in ind["products"])
        rows.append('<li><h3 class="p-iname">%s</h3><p class="p-iline">%s</p><div class="p-ilinks">%s</div></li>' % (T(*ind["name"]), T(*ind["line"], bind=3), links))
    h = head(T("Solutions", "Giải pháp"), T("Industries", "Ngành công nghiệp"), T(*C.INDUSTRIES_LEDE, bind=3), hid="p-h-ind")
    return '<section class="p-sec" id="industries" aria-labelledby="p-h-ind"><div class="p-wrap">%s<ul class="p-ind">%s</ul></div></section>' % (h, "".join(rows))


def sec_services():
    frames = "".join('<li class="p-frame"><span class="p-fn">0%d</span><span class="p-ft">%s</span></li>' % (i + 1, T(*s)) for i, s in enumerate(C.STEPS))
    h = head(T("Services", "Dịch vụ"), T(*C.SERVICES_H), T(*C.SERVICES_LEDE, bind=3), hid="p-h-svc")
    more = '<div class="p-wrap p-svcfoot">%s</div>' % A(C.SERVICES_MORE, '<span>%s</span>%s' % (T(*SEE_SERVICES), ARROW), "p-more")
    return ('<section class="p-sec p-svc" id="services" aria-labelledby="p-h-svc"><div class="p-wrap">%s</div><ol class="p-strip">%s</ol>%s</section>' % (h, frames, more))


def sec_customers():
    li = "".join('<li><img src="assets/logos/%s" alt="%s" width="%d" height="%d"></li>' % (f, esc(n), *Image.open(os.path.join(ASSETS, "logos", f)).size) for f, n in C.LOGOS)
    h = head(T("Customers", "Khách hàng"), T(*C.CLIENTS_H), esc(CLAIM), hid="p-h-cust")
    return '<section class="p-sec" id="customers" aria-labelledby="p-h-cust"><div class="p-wrap">%s<ul class="p-sheet">%s</ul></div></section>' % (h, li)


def mean_lum(path):
    return float(np.asarray(Image.open(path).convert("L")).mean())


def sec_news():
    rows = []
    for i, n in enumerate(C.NEWS):
        bright = mean_lum(os.path.join(ASSETS, "news", n["img"])) > 120
        rows.append('<div class="p-nitem" role="listitem" style="--o:%d;--ov:%d">%s</div>' % (i + 1, n["vi_order"], A(n["url"],
                    '<span class="p-nimg%s"><img src="assets/news/%s" width="960" height="720" alt=""></span><span class="p-ntxt"><span class="p-date">%s</span><span class="p-ntitle">%s</span><span class="p-nmore"><span>%s</span>%s</span></span>'
                    % (" p-bright" if bright else "", n["img"], T(*n["date"]), T(*n["title"], bind=3), T(*READ_MORE), ARROW), "p-nl")))
    h = head(T("News", "Tin tức"), T(*C.NEWS_H), hid="p-h-news")
    more = '<p class="p-after">%s</p>' % A(C.NEWS_ALL, '<span>%s</span>%s' % (T(*VIEW_ALL), ARROW), "p-more")
    return '<section class="p-sec" id="news" aria-labelledby="p-h-news"><div class="p-wrap">%s<div class="p-news" role="list">%s</div>%s</div></section>' % (h, "".join(rows), more)


def waveform():
    """The hero's material: cream to amber bars with a soft reflection on a floor line."""
    rnd = random.Random(11)
    W, Hh, cy, floor = 1920, 215, 84, 162
    bumps = [(210, 70, .5), (470, 55, .85), (560, 40, .6), (800, 90, .45), (1060, 65, 1.0), (1150, 40, .7), (1400, 60, .75), (1690, 80, .55)]
    segs = []
    x = 3.0
    while x < W:
        env = .05 + sum(a * math.exp(-((x - c) / s) ** 2) for c, s, a in bumps)
        amp = min(1.0, env) * (0.35 + 0.65 * rnd.random()) * 72
        segs.append("M%.1f %.1fV%.1f" % (x, cy - amp, cy + amp))
        x += 6
    d = "".join(segs)
    return ('<svg class="p-wave" viewBox="0 0 %d %d" preserveAspectRatio="xMidYMax slice" aria-hidden="true" focusable="false">'
            '<defs><linearGradient id="p-wg" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".14" stop-color="#fff"/><stop offset=".86" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            '<linearGradient id="p-wc" gradientUnits="userSpaceOnUse" x1="0" x2="0" y1="10" y2="158"><stop offset="0" stop-color="#F1E6D0"/><stop offset=".55" stop-color="#E9CD9A"/><stop offset="1" stop-color="#C98B3F"/></linearGradient>'
            '<linearGradient id="p-wf" gradientUnits="userSpaceOnUse" x1="0" x2="0" y1="%d" y2="%d"><stop offset="0" stop-color="#fff" stop-opacity=".9"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            '<mask id="p-wm"><rect width="%d" height="%d" fill="url(#p-wg)"/></mask><mask id="p-wr"><rect width="%d" height="%d" fill="url(#p-wg)"/><rect y="%d" width="%d" height="%d" fill="url(#p-wf)" style="mix-blend-mode:multiply"/></mask></defs>'
            '<g mask="url(#p-wm)"><path d="%s" fill="none" stroke="url(#p-wc)" stroke-width="2.2" stroke-linecap="round" vector-effect="non-scaling-stroke"/></g>'
            '<g mask="url(#p-wm)" opacity=".2" transform="translate(0 %d) scale(1 -.3) translate(0 %d)"><path d="%s" fill="none" stroke="url(#p-wc)" stroke-width="2.2" stroke-linecap="round" vector-effect="non-scaling-stroke"/></g>'
            '<path d="M0 %d H%d" stroke="#E9CD9A" stroke-opacity=".28" stroke-width="1" vector-effect="non-scaling-stroke" mask="url(#p-wm)"/></svg>'
            % (W, Hh, floor, Hh, W, Hh, W, Hh, floor, W, Hh - floor, d, floor, floor, d, floor, W))


def sec_cta():
    phone = A((C.PHONE_TEL[0], C.PHONE_TEL[1]), '<span class="en">%s</span><span class="vi">%s</span>' % (esc(C.PHONE[0]), esc(C.PHONE[1])), "btn btn-line", blank=False)
    contact = A(C.CONTACT_URL, '<span>%s</span>' % T("Contact", "Liên hệ"), "btn btn-white")
    head_ = ('<div class="p-head p-chead"><p class="p-eye p-ceye">%s%s</p><div class="p-hbody"><h2 class="p-h2 p-ctah" id="p-h-cta"><span lang="en">%s</span></h2><p class="p-lede p-ctasub">%s</p>'
             '<div class="p-ctabtns">%s%s</div></div></div>' % (dia(), T("Contact", "Liên hệ"), fmt(C.CTA_H[0], "en", 3), T(*C.CTA_SUB, bind=3), contact, phone))
    return ('<section class="p-cta" id="contact" aria-labelledby="p-h-cta"><img class="p-ctabg" src="assets/b/sky.jpg" width="1600" height="640" alt="">%s'
            '<div class="p-wrap">%s</div></section>' % (waveform(), head_))


def footer():
    links = "".join('<li>%s</li>' % A(u, T(*n), blank=True) for n, u in C.FOOT_LINKS)
    social = "".join('<li><a href="%s" target="_blank" rel="noopener">%s</a></li>' % (u, n) for n, u in C.SOCIAL)
    offices = "".join('<div><b>%s</b>%s</div>' % (T(n_en, n_vi), T(a_en, a_vi)) for n_en, n_vi, a_en, a_vi in C.OFFICES)
    tel = '<a href="%s" data-en="%s" data-vi="%s"><span class="en">%s</span><span class="vi">%s</span></a>' % (C.PHONE_TEL[0], C.PHONE_TEL[0], C.PHONE_TEL[1], esc(C.PHONE[0]), esc(C.PHONE[1]))
    lw = Image.open(os.path.join(ASSETS, "brand", "logo-white.png")).size
    return ('<footer class="p-foot"><div class="p-wrap"><div class="p-fgrid">'
            '<div><img class="p-flogo" src="assets/brand/logo-white.png" alt="Aimesoft" width="%d" height="26"><div class="p-fcontact">%s<a href="mailto:%s">%s</a></div></div>'
            '<nav aria-label="Footer" data-aria-en="Footer" data-aria-vi="Chân trang"><p class="p-fh">%s</p><ul class="p-flist">%s</ul></nav>'
            '<div><p class="p-fh">%s</p><address class="p-off">%s</address></div>'
            '<div><p class="p-fh">%s</p><ul class="p-flist">%s</ul></div>'
            '</div><p class="p-copy">%s</p></div></footer>'
            % (round(26 * lw[0] / lw[1]), tel, C.EMAIL, C.EMAIL, T("Aimesoft", "Aimesoft"), links, T("Offices", "Văn phòng"), offices, T("Follow", "Theo dõi"), social, fmt(C.COPY, "en", 3)))


# ---- gates inside the generator
def css_rules(css):
    """Top-level selectors (depth 0) of a stylesheet, comments stripped."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    out, depth, buf = [], 0, ""
    for ch in css:
        if ch == "{":
            if depth == 0:
                out.append(buf.strip())
            depth += 1; buf = ""
        elif ch == "}":
            depth -= 1; buf = ""
        elif depth == 0:
            buf += ch
    return out


def gate_css(full_css):
    a, b = full_css.index("/*PAGE-CSS-START*/"), full_css.index("/*PAGE-CSS-END*/")
    page, hero = full_css[a:b], full_css[:a]
    ps = [s.strip() for r in css_rules(page) if not r.startswith("@") for s in r.split(",")]
    hs = {s.strip() for r in css_rules(hero) if not r.startswith("@") for s in r.split(",")}
    dup = {s for s in ps if ps.count(s) > 1}
    assert not dup, "selector declared twice in page CSS: %s" % sorted(dup)
    allowed = {"html", ":root"}
    for s in ps:
        assert s in allowed or ".p-" in s, "page selector without p- prefix: " + s
        assert s in allowed or s not in hs, "page selector collides with the hero CSS: " + s
    for m in re.finditer(r"@media[^{]+\{(.*?)\n\}", page, flags=re.S):
        for sel in re.findall(r"(?:^|\})\s*([^{}@]+)\{", m.group(1)):
            for s in sel.split(","):
                s = s.strip()
                assert (not s) or s in allowed or ".p-" in s, "media selector without p-: " + s
    print("css gate: %d page selectors, no duplicates, all p- prefixed" % len(ps))


FORBIDDEN_WORDS = re.compile(r"minh ho[aạ]|\bdemo\b|placeholder|\bsample\b|lorem|Tristan|Leo\b|Iris|Owl|Lewis|Oscar|BACKEND|prefix|approved", re.I)
FORBIDDEN_CHARS = "—–·•…“”‘’→"


def gate_text(html_text):
    body = re.sub(r"<style.*?</style>|<script.*?</script>", "", html_text, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", body)
    m = FORBIDDEN_WORDS.search(text)
    assert not m, "forbidden word on the page: " + m.group(0)
    bad = sorted({c for c in html_text if c in FORBIDDEN_CHARS})
    assert not bad, "forbidden characters: %r" % bad
    for em in re.findall(r"[\U0001F300-\U0001FAFF☀-➿]", html_text):
        raise AssertionError("emoji: " + em)
    assert not re.search(r"\d\s?%|confidence|score|accuracy of \d", " ".join(re.findall(r"<svg.*?</svg>", html_text, flags=re.S))), "an overlay carries a figure"


def strip_comments(t):
    t = re.sub(r"<!--.*?-->", "", t, flags=re.S)
    def css(m):
        return m.group(1) + re.sub(r"/\*.*?\*/", "", m.group(2), flags=re.S) + m.group(3)
    t = re.sub(r"(<style>)(.*?)(</style>)", css, t, flags=re.S)
    def js(m):
        body = re.sub(r"(?m)^\s*//.*$", "", m.group(2)); body = re.sub(r"/\*.*?\*/", "", body, flags=re.S)
        return m.group(1) + body + m.group(3)
    t = re.sub(r"(<script>)(.*?)(</script>)", js, t, flags=re.S)
    assert "/*" not in t and "<!--" not in t, "comment left in the page"
    return t


def main():
    os.makedirs(OUT, exist_ok=True)
    bg, bgc = hero_bg()
    css_fonts = "\n".join(open(os.path.join(APPROVED, "assets", "fonts-css", n + ".css")).read() for n in ("intertight", "geistmono"))
    lw = round(26 * Image.open(os.path.join(ASSETS, "brand", "logo-white.png")).size[0] / Image.open(os.path.join(ASSETS, "brand", "logo-white.png")).size[1])
    nav = "\n".join('        <a href="%s"><span class="en">%s</span><span class="vi">%s</span></a>' % (a, esc(e), esc(v)) for a, e, v in C.NAV)
    leads = "".join('<i class="lead" style="--x:%d;--y1:%d;--y2:%d"></i>' % tuple(l) for l in CFG.get("leads", []))
    gpt = [p for p in C.PRODUCTS if p["key"] == "gpt"][0]["url"]
    t = open(os.path.join(HERE, "b.page.tpl.html"), encoding="utf-8").read()
    sections = "\n".join((sec_products(), sec_numbers(), sec_industries(), sec_services(), sec_customers(), sec_news(), sec_cta()))
    t = (t.replace("@@FONTS@@", css_fonts).replace("@@BG@@", bg).replace("@@STAGE_H@@", str(CFG["stage_h"])).replace("@@IDX_TOP@@", str(CFG["idx_top"]))
          .replace("@@POS_WIDE@@", CFG["pos_wide"]).replace("@@POS_PORT@@", CFG["pos_port"]).replace("@@LOGO_W@@", str(lw))
          .replace("@@NAV@@", nav).replace("@@LEADS@@", leads).replace("@@GPT_EN@@", gpt[0]).replace("@@GPT_VI@@", gpt[1])
          .replace("@@SECTIONS@@", sections).replace("@@FOOTER@@", footer()))
    t = nb(t)
    assert "@@" not in t, "unreplaced placeholder"
    gate_css(t[t.index("<style>"): t.index("</style>")])
    gate_text(t)
    t = strip_comments(t)
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(t)
    open(os.path.join(OUT, "CNAME"), "w").write(DOMAIN + "\n")
    open(os.path.join(OUT, ".nojekyll"), "w").write("")
    used = set(re.findall(r'(?:src|href)="(assets/[^"]+)"', t))
    for rel in sorted(used):
        src = os.path.join(ROOT, rel)
        assert os.path.exists(src), "missing asset " + rel
        dst = os.path.join(OUT, rel); os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copy(src, dst)
    for dp, dn, fn in os.walk(os.path.join(OUT, "assets")):
        for f in fn:
            rel = os.path.relpath(os.path.join(dp, f), OUT)
            if rel not in used:
                os.remove(os.path.join(dp, f))
    print("built B v%s bg %s, %d assets, %d KB html" % (VERSION, bg, len(used), os.path.getsize(os.path.join(OUT, "index.html")) // 1024))


if __name__ == "__main__":
    main()
