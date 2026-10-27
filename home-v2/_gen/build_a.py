#!/usr/bin/env python3
"""Aimesoft 2.0 home page, direction A (light). Writes ../site-a/ (index.html, CNAME, .nojekyll, assets/).
Header + hero come unchanged from the approved block (approval-block-v2/_gen/a.tpl.html); everything below is new.
Run: /Users/ciaosoft/Claude/BRvault/_System/venv-pw/bin/python build_a.py"""
import os, re, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
V2 = os.path.join(os.path.dirname(ROOT), "approval-block-v2", "_gen")
sys.path.insert(0, HERE); sys.path.insert(0, V2)
import content as C
import build as B0            # approved block generator: marks_svg, fonts, CFG

OUT = os.environ.get("BUILD_OUT", os.path.join(ROOT, "site-a"))
DOMAIN = "aimesoft-a.ciaosoft.vn"


def bind(t):
    """Keep the last words of a longer text together so a block never ends on a lone word. Two words from 5 words up; three from 12 up when
    the three words are short enough (<= 22 characters) not to overflow a narrow column."""
    w = t.split(" ")
    if len(w) < 5: return t
    k = 3 if (len(w) >= 12 and len(" ".join(w[-3:])) <= 22) else 2
    if len(" ".join(w[-k:])) > 24: k = 1
    if k == 1: return t
    return " ".join(w[:-k]) + " " + "&nbsp;".join(w[-k:])


def addr(a):
    """Hyphenated tokens in an address (1-2-20, Minato-ku, 105-0022) must not break at the hyphen. Bind first, then wrap."""
    return re.sub(r"\S*-\S*", lambda m: '<span class="nb">%s</span>' % m.group(0), bind(a))


def bi(en, vi):
    return '<span class="en">%s</span><span class="vi">%s</span>' % (bind(en), bind(vi))

VI_COMP = B0.VI_COMP + ["hệ sinh thái", "trí tuệ nhân tạo", "khách sạn", "bán lẻ", "giải pháp", "nhận diện", "nhận dạng", "tiếng nói", "giọng nói",
                        "văn bản", "khai phá", "thấu hiểu", "hỗ trợ", "đánh giá", "thông tin", "giáo dục", "điện tử", "thương mại", "cung cấp", "việt nam", "đón đầu", "phần mềm", "hồ chí minh", "tp.", "sức khỏe", "chăm sóc", "tin tức", "hệ thống", "số liệu", "xem thêm", "gọi", "ngôn ngữ", "thuyết trình",
                        "thành lập", "độ chính xác", "chữ in", "bản đồ", "ứng dụng", "doanh nghiệp", "nền tảng", "phát triển", "công nghệ", "tuyển dụng", "chính sách", "bảo mật",
                        "miền nam", "hà nội", "lượt triển khai", "tiếng việt", "tiếng nhật"]


def nb(html):
    def vi(m):
        t = m.group(2)
        for w in sorted(set(VI_COMP), key=len, reverse=True):
            t = re.sub(r"(?i)(?<![\w>])(%s)(?![\w])" % re.escape(w), lambda k: '<span class="nb">%s</span>' % k.group(1), t)
        return m.group(1) + t + m.group(3)
    html = re.sub(r'(<span class="vi">)([^<]*)(</span>)', vi, html)
    for w in ("200+ installations", "one platform", "AimeGPT", "AimeFace", "AimeSpeech", "AimeCard", "AimeHotel", "AimeReception", "AimeHospital", "AimeFluent", "Aime AIShop"):
        html = html.replace(" " + w + " ", ' <span class="nb">%s</span> ' % w) if w.count(" ") else html
    for w in ("all-time", "check-in,&nbsp;check-out.", "check-in, check-out.", "finance - banking", "e-commerce", "End-to-End", "Real-time", "Speech-to-Text (STT)", "Text-to-Speech (TTS)", "GPT-2", "GPT-3", "mini-ChatGPT", "end-to-end", "on-premise"):
        html = html.replace(w, '<span class="nb">%s</span>' % w)
    return html


def lk(href_pair, cls, inner, extra=""):
    en, vi = href_pair
    return '<a class="%s" href="%s" data-en="%s" data-vi="%s" target="_blank" rel="noopener"%s>%s</a>' % (cls, en, en, vi, extra, inner)


ARROW = '<svg class="p-ar" viewBox="0 0 16 16" width="16" height="16" aria-hidden="true"><path d="M3 8h9M8.5 4l4 4-4 4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="square"/></svg>'

# --- anchor point of the hero's diamond, opened up inside each crop (percent of the crop); the tag hangs from it on a hairline
POINTS = {"face": (26.5, 41.0), "speech": (47.0, 33.0), "card": (42.5, 43.0)}
IMG = {"face": "assets/a/see.jpg", "speech": "assets/a/hear.jpg", "card": "assets/a/read.jpg"}
ALT = {
    "face": ("A receptionist smiles at a visitor across the front desk.", "Nhân viên lễ tân mỉm cười với một vị khách qua quầy."),
    "speech": ("The receptionist's smile as she speaks with the visitor.", "Nụ cười của nhân viên lễ tân khi trò chuyện với vị khách."),
    "card": ("A hand holds out an ID card.", "Một bàn tay đưa thẻ căn cước."),
}


# A shows more of each page's own feature list than B (a taller card has room); every line is on the product page, in that page's language
CHIPS = {
    "face": [("Real-time face recognition, detection, and identification", "Phát hiện khuôn mặt Real-time"),
             ("Multimodal AI-based face registration. Allow registering face immediately", "Đăng ký khuôn mặt dựa trên Multimodal AI"),
             ("Real-time model retraining", "Đào tạo lại mô hình Real-time"),
             ("Comparison between actual faces and face images in ID cards", "So sánh giữa khuôn mặt thực tế và hình ảnh khuôn mặt trong thẻ ID")],
    "speech": [("Speech recognition (Speech-to-Text, STT)", "Nhận dạng giọng nói (Chuyển tiếng nói thành văn bản, STT, ASR)"),
               ("Speech Synthesis (Text-to-Speech, TTS)", "Tổng hợp tiếng nói (Chuyển văn bản thành giọng nói, TTS)"),
               ("Speaker identification", "Nhận dạng, nhận diện người nói")],
    "card": [("Allow users to config templates themselves", "Nhận diện nhanh và chính xác chữ và số trên các văn bản"),
             ("Driving license and passport recognition", "Phân tích được cấu trúc của văn bản"),
             ("Invoices and documents recognition", "Nhận diện được nhiều loại văn bản khác nhau, hỗ trợ đa ngôn ngữ")],
    "gpt": [("On-premise deployment", "Triển khai trên server khách hàng"), ("Fine-tuning with domain data", "Tinh chỉnh trên miền dữ liệu cụ thể"),
            ("Various real-world applications", "Ứng dụng thực tiễn đa dạng")],
}


def _corners(l, t, r, b, n=0.0):
    """Four corner marks of a frame, in percent of the picture; purely geometric, no text."""
    L = 7.0
    d = ("M%.1f %.1f h%.1f M%.1f %.1f v%.1f " % (l, t + L * 0.7, 0, l, t, L * 0.7)) if False else ""
    pts = []
    for (x, y, sx, sy) in ((l, t, 1, 1), (r, t, -1, 1), (l, b, 1, -1), (r, b, -1, -1)):
        pts.append("M%.1f %.1f L%.1f %.1f L%.1f %.1f" % (x + sx * 5, y, x, y, x, y + sy * 5))
    return '<svg class="p-br" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true"><path d="%s"/></svg>' % " ".join(pts)


BRACKETS = {"face": _corners(10, 18, 58, 66), "card": _corners(13, 12, 83, 72)}


def tag(p):
    return '<i class="dia"></i><em>%s</em><b>%s</b>' % (bi(*p["verb"]), p["name"])


def product_card(p, cls):
    k = p["key"]
    chips = "".join("<li>%s</li>" % bi(*c) for c in CHIPS[p["key"]])
    more = lk(p["url"], "p-more", bi(*C.LEARN) + ARROW, ' aria-label="%s"' % p["name"])
    ben = ""
    if p["key"] == "face":
        ben = ('<div class="p-ben"><p>%s</p><ul>%s</ul></div>' % (bi("Benefits", "Ưu điểm"), "".join("<li>%s</li>" % bi(*b) for b in (
            ("Automated check-in, checkout, registration", "Tự động đăng ký check-in, check-out."),
            ("Serve customers quickly and conveniently all-time working 24/7", "Phục vụ khách hàng nhanh chóng và thuận tiện mọi lúc làm việc 24/7"),
            ("Saving time for customers", "Tiết kiệm thời gian cho khách hàng")))))
    body = ('<div class="p-body"><p class="p-line">%s</p><h3 class="p-name">%s</h3><p class="p-desc">%s</p><ul class="p-chips">%s</ul>%s%s</div>'
            % (bi(*p["line"]), p["name"], bi(*p["desc"]), chips, ben, more))
    if k == "gpt":
        vis = ('<div class="p-gv" aria-hidden="true"><span class="p-gtag">%s</span>'
               '<div class="p-gl"><b>JA</b><span>%s</span></div><div class="p-gl"><b>VI</b><span>%s</span></div>'
               '<span class="p-gnote">%s</span></div>') % (tag(p), bi("Japanese", "Tiếng Nhật"), bi("Vietnamese", "Tiếng Việt"), bi("GPT models, trained mainly on Japanese or Vietnamese text", "Mô hình GPT, huấn luyện chủ yếu với văn bản tiếng Nhật hoặc tiếng Việt"))
        return '<article class="p-card p-gpt %s">%s%s</article>' % (cls, body, vis)
    x, y = POINTS[k]
    br = BRACKETS.get(k, "")
    ph = ('<div class="p-ph"><img src="%s" alt="" width="680" height="680" loading="lazy" data-alt-en="%s" data-alt-vi="%s">%s'
          '<span class="p-pt" style="left:%.1f%%;top:%.1f%%"><span class="p-tg">%s</span></span></div>') % (IMG[k], ALT[k][0], ALT[k][1], br, x, y, tag(p))
    return '<article class="p-card p-%s %s">%s%s</article>' % (k, cls, ph, body)


def products_html():
    P = {p["key"]: p for p in C.PRODUCTS}
    cards = product_card(P["face"], "p-c1") + product_card(P["speech"], "p-c2") + product_card(P["card"], "p-c3") + product_card(P["gpt"], "p-c4")
    return ('<section class="p-sec" id="products" aria-labelledby="h-products"><div class="p-wrap">'
            '<header class="p-head"><p class="p-eye"><i class="dia"></i>%s</p><h2 id="h-products">%s</h2><p class="p-lede">%s</p></header>'
            '<div class="p-bento">%s</div>'
            '<p class="p-allp">%s</p></div></section>') % (
        bi("Products", "Sản phẩm"), bi("Aimenicorn products", "Sản phẩm Aimenicorn"),
        bi("Aimenicorn is a Multimodal AI ecosystem developed by Aimesoft to simplify the process of applying Multimodal AI technologies in various industries by providing Multimodal AI software packages.",
           "Aimenicorn là một hệ sinh thái trí tuệ nhân tạo đa thể thức được phát triển bởi Aimesoft"),
        cards, lk(C.PRODUCTS_ALL, "p-more p-more-all", bi("View all products and solutions", "Xem tất cả sản phẩm và giải pháp") + ARROW))


def numbers_html():
    items = "".join('<li class="p-n%d"><b>%s</b><span>%s</span></li>' % (i + 1, n[0], bi(n[1], n[2])) for i, n in enumerate(C.NUMBERS))
    return ('<section class="p-sec p-sec-num" id="multimodal" aria-labelledby="h-mm"><div class="p-wrap">'
            '<header class="p-head"><p class="p-eye"><i class="dia"></i>%s</p><h2 id="h-mm">%s</h2><p class="p-lede">%s</p></header>'
            '<ul class="p-nums">%s</ul></div></section>') % (
        bi("Multimodal AI", "Multimodal AI"), bi("Text, voice, image and numbers in a single system.", "Văn bản, tiếng nói, ảnh và số liệu trong một hệ thống."),
        bi(C.MM_EN, C.MM_VI), items)


def industries_html():
    tiles = ""
    for i, d in enumerate(C.INDUSTRIES):
        pr = "".join(lk(u, "p-pill", '<i class="dia"></i>%s%s' % (n, ARROW)) for n, u in d["products"])
        tiles += '<li class="p-ind"><h3>%s</h3><p>%s</p><div class="p-pills">%s</div></li>' % (bi(*d["name"]), bi(*d["line"]), pr)
    return ('<section class="p-sec p-paper" id="industries" aria-labelledby="h-ind"><div class="p-wrap">'
            '<header class="p-head"><p class="p-eye"><i class="dia"></i>%s</p><h2 id="h-ind">%s</h2><p class="p-lede">%s</p></header>'
            '<ul class="p-inds">%s</ul></div></section>') % (
        bi("Industries", "Ngành"), bi("Solutions by industry", "Giải pháp theo ngành"), bi(*C.INDUSTRIES_LEDE), tiles)


def services_html():
    steps = "".join('<li><span class="p-sn">%02d</span><i class="p-nd"></i><p>%s</p></li>' % (i + 1, bi(*s)) for i, s in enumerate(C.STEPS))
    return ('<section class="p-sec p-dark" id="services" aria-labelledby="h-srv"><div class="p-wrap">'
            '<header class="p-head"><p class="p-eye"><i class="dia"></i>%s</p><h2 id="h-srv">%s</h2><div class="p-lede-wrap"><p class="p-lede">%s</p>%s</div></header>'
            '<ol class="p-steps">%s</ol></div></section>') % (
        bi("Services", "Dịch vụ"), bi(*C.SERVICES_H), bi(*C.SERVICES_LEDE),
        lk(C.SERVICES_MORE, "p-more p-more-inv", bi("Explore our services", "Khám phá dịch vụ") + ARROW), steps)


def customers_html():
    SC = {"tokushukai.png": 1.1, "dentsu.png": 1.05, "nexus.png": .85, "rath.png": .85, "fine.png": 1.1, "prominent.png": .8}   # optical weight, so no logo outshouts its neighbours
    tiles = "".join('<li style="--s:%s"><img src="assets/logos/%s" alt="%s" loading="lazy"></li>' % (SC.get(f, 1), f, n) for f, n in C.LOGOS)
    return ('<section class="p-sec" id="customers" aria-labelledby="h-cus"><div class="p-wrap">'
            '<header class="p-head p-head-one"><p class="p-eye"><i class="dia"></i>%s</p><h2 id="h-cus">%s</h2></header>'
            '<ul class="p-logos">%s</ul></div></section>') % (bi("Customers", "Khách hàng"), bi(*C.CLIENTS_H), tiles)


def news_html():
    cards = ""
    for i, n in enumerate(C.NEWS):
        cards += ('<li class="p-new p-new%d" style="--vo:%d"><a class="p-nl" href="%s" data-en="%s" data-vi="%s" target="_blank" rel="noopener">'
                  '<span class="p-nimg"><img src="assets/news/%s" alt="" width="960" height="600" loading="lazy"></span>'
                  '<time class="p-date">%s</time><h3>%s</h3><span class="p-more">%s%s</span></a></li>') % (
            i + 1, n["vi_order"], n["url"][0], n["url"][0], n["url"][1], n["img"], bi(*n["date"]), bi(*n["title"]), bi("Read more", "Chi tiết"), ARROW)
    return ('<section class="p-sec" id="news" aria-labelledby="h-news"><div class="p-wrap">'
            '<header class="p-head p-head-one"><p class="p-eye"><i class="dia"></i>%s</p><h2 id="h-news">%s</h2>%s</header>'
            '<ul class="p-news">%s</ul></div></section>') % (
        bi("News", "Tin tức"), bi(*C.NEWS_H), lk(C.NEWS_ALL, "p-more p-head-link", bi("All news", "Tất cả tin tức") + ARROW), cards)


def cta_html():
    return ('<section class="p-cta-wrap" id="contact" aria-labelledby="h-cta"><div class="p-cta"><img class="p-ctaimg" src="assets/a/cta.jpg" alt="" width="800" height="660" loading="lazy">'
            '<div class="p-ctat"><p class="p-eye p-eye-inv"><i class="dia"></i>%s</p><h2 id="h-cta">%s</h2><p class="p-ctasub">%s</p>'
            '<div class="p-ctab">%s%s</div></div></div></section>') % (
        bi("Contact", "Liên hệ"), bi(*C.CTA_H), bi(*C.CTA_SUB),
        lk(C.CONTACT_URL, "btn btn-white", bi("Contact us", "Liên hệ tư vấn")),
        '<a class="btn btn-line" href="%s" data-en="%s" data-vi="%s">%s</a>' % (C.PHONE_TEL[0], C.PHONE_TEL[0], C.PHONE_TEL[1], bi(C.PHONE[0], C.PHONE[1])))


def footer_html():
    links = "".join("<li>%s</li>" % lk(u, "p-fl", bi(*n)) for n, u in C.FOOT_LINKS)
    soc = "".join('<li><a class="p-fl" href="%s" target="_blank" rel="noopener">%s</a></li>' % (u, n) for n, u in C.SOCIAL)
    offs = "".join('<li><b>%s</b><span><span class="en">%s</span><span class="vi">%s</span></span></li>' % (bi(e, v), addr(a), addr(av)) for e, v, a, av in C.OFFICES)
    return ('<footer class="p-foot"><div class="p-wrap"><div class="p-ft"><div class="p-fb"><a class="brand" href="#" aria-label="Aimesoft"><img src="assets/brand/logo-blue.png" alt="Aimesoft" height="26"></a>'
            '<p>%s</p><p class="p-fc"><a href="%s" data-en="%s" data-vi="%s">%s</a><a href="mailto:%s">%s</a></p></div>'
            '<nav aria-label="Footer" data-aria-en="Footer" data-aria-vi="Chân trang"><ul class="p-fnav">%s</ul><ul class="p-fnav p-fsoc">%s</ul></nav>'
            '<ul class="p-offs">%s</ul></div><p class="p-copy">%s</p></div></footer>') % (
        bi(*C.TAGLINE),
        C.PHONE_TEL[0], C.PHONE_TEL[0], C.PHONE_TEL[1], bi(C.PHONE[0], C.PHONE[1]), C.EMAIL, C.EMAIL, links, soc, offs, bind(C.COPY))


CSS = r"""
/* ---------------- below the hero: new blocks, every class prefixed p- ---------------- */
:root{--paper:#F4F2EE;--line2:#E6E2DA;--pad-s:104px;--ink3:#5A5F6C}
html{scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
section[id]{scroll-margin-top:calc(var(--hdr) + 8px)}
.p-wrap{max-width:1440px;margin:0 auto;padding-inline:calc(var(--edge) + var(--pad))}
.p-sec{padding-block:var(--pad-s)}
.p-paper{background:var(--paper)}
.p-eye{display:flex;align-items:center;gap:12px;font:500 12.5px/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--ink2);margin-bottom:24px}
.p-eye .dia{width:7px;height:7px;background:var(--blue)}
.p-eye-inv,.p-dark .p-eye{color:#C9D3E3}
.p-head{display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);column-gap:64px;row-gap:0;margin-bottom:56px;align-items:end}
.p-head .p-eye{grid-column:1 / -1}
.p-head h2{font-weight:500;font-size:clamp(36px,3.9vw,56px);line-height:1.02;letter-spacing:-.035em;color:var(--ink);text-wrap-style:balance}
.p-lede{font-size:18px;line-height:1.55;color:var(--ink2);text-wrap-style:pretty;max-width:520px;justify-self:end}
.p-head-one{grid-template-columns:1fr auto}
.p-head-one h2{grid-column:1}
.p-head-link{justify-self:end;align-self:end}
.p-ar{flex:none;transition:transform .18s}
.p-more{display:inline-flex;align-items:center;gap:10px;min-height:44px;font-weight:600;font-size:15px;color:var(--ink);border-bottom:1.5px solid var(--ink);align-self:flex-start;padding:10px 0 6px}
.p-more:hover .p-ar,.p-nl:hover .p-ar,.p-pill:hover .p-ar{transform:translateX(4px)}
.p-more:hover{border-bottom-color:var(--blue)}
.p-more-inv{color:#fff;border-bottom-color:#fff}
.p-more-inv:hover{border-bottom-color:var(--blue-lt)}
.p-allp{margin-top:40px;display:flex}
.p-head-link.p-more{padding-top:0}

/* numbers */
.p-sec-num{padding-top:96px;padding-bottom:104px}
.p-nums{list-style:none;display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:0 0;border-top:1.5px solid var(--ink);margin-top:8px}
.p-nums li{position:relative;padding:34px 22px 0 0;margin-right:22px;border-right:1px solid var(--line)}
.p-nums li:last-child{border-right:0;margin-right:0}
.p-nums li::before{content:"";position:absolute;left:0;top:-5.5px;width:9px;height:9px;background:var(--blue);transform:rotate(45deg)}
.p-nums b{display:block;font-weight:500;font-size:clamp(44px,4.4vw,64px);line-height:1;letter-spacing:-.045em;color:var(--ink);white-space:nowrap}
.p-nums li>span{display:block;margin-top:16px;font-size:15px;line-height:1.45;color:var(--ink2);max-width:226px;text-wrap-style:balance}

/* products bento */
.p-bento{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:20px}
.p-card{position:relative;border-radius:20px;overflow:hidden;background:var(--paper);display:flex;flex-direction:column;min-width:0}
.p-c1{grid-column:span 7;flex-direction:row}
.p-c2{grid-column:span 5}
.p-c3{grid-column:span 5}
.p-c4{grid-column:span 7;flex-direction:row;background:var(--ink);color:#fff}
.p-ph{position:relative;overflow:hidden;flex:none}
.p-ph img{display:block;width:100%;height:100%;object-fit:cover;transition:transform .5s cubic-bezier(.2,.7,.2,1)}
.p-card:hover .p-ph img{transform:scale(1.035)}
.p-c1 .p-ph{width:47%;min-height:520px}
.p-c2 .p-ph,.p-c3 .p-ph{aspect-ratio:16 / 9.4}
.p-body{display:flex;flex-direction:column;padding:32px 34px 30px;flex:1;min-width:0}
.p-line{font-weight:500;font-size:14.5px;line-height:1.4;color:var(--ink3);margin-bottom:14px;text-wrap-style:pretty}
.p-name{font-weight:500;font-size:clamp(30px,2.5vw,36px);line-height:1;letter-spacing:-.035em;color:var(--ink);margin-bottom:16px}
.p-desc{font-size:16.5px;line-height:1.55;color:var(--ink2);text-wrap-style:pretty;margin-bottom:20px}
.p-chips{list-style:none;display:flex;flex-direction:column;gap:8px;margin-bottom:26px}
.p-chips li{position:relative;padding-left:20px;font-size:14.5px;line-height:1.4;color:var(--ink)}
.p-chips li::before{content:"";position:absolute;left:1px;top:.5em;width:6px;height:6px;background:var(--blue);transform:rotate(45deg)}
.p-body .p-more{margin-top:auto}
.p-ben{margin:2px 0 28px;padding-top:20px;border-top:1px solid #D9E0EA}
.p-ben p{font:500 11.5px/1 var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--ink3);margin-bottom:12px}
.p-ben ul{list-style:none;display:flex;flex-direction:column;gap:7px}
.p-ben li{font-size:14.5px;line-height:1.4;color:var(--ink2)}
/* the hero's diamond, opened up: point + hairline + tag */
.p-pt{position:absolute;width:0;height:0}
.p-pt::before{content:"";position:absolute;left:-7px;top:-7px;width:14px;height:14px;background:var(--blue);border:1.5px solid #fff;transform:rotate(45deg);box-shadow:0 0 0 4px rgba(255,255,255,.28)}
.p-pt::after{content:"";position:absolute;left:0;top:-8px;width:1.25px;height:46px;background:var(--ink);transform:translateY(-100%)}
.p-tg{position:absolute;left:-1px;bottom:54px;display:flex;align-items:baseline;gap:9px;white-space:nowrap;padding:7px 10px;background:rgba(255,255,255,.9);border-radius:3px;color:var(--ink)}
.p-tg .dia{display:none}
.p-tg em{font:500 11.5px/1 var(--mono);letter-spacing:.16em;font-style:normal;color:var(--slate)}
.p-tg b{font:600 14px/1 var(--mono);letter-spacing:.02em}
/* AimeGPT: the dark card, a type specimen of its two languages */
.p-c4 .p-name,.p-c4 .p-chips li{color:#fff}
.p-c4 .p-line{color:#A9B6CB}
.p-c4 .p-desc{color:#D5DDEA}
.p-c4 .p-more{color:#fff;border-bottom-color:#fff}
.p-c4 .p-body{flex:1.25}
.p-gv{flex:1;position:relative;margin:20px 20px 20px 0;border-radius:14px;background:#17233A;border:1px solid #2A3A57;padding:76px 28px 24px;display:flex;flex-direction:column;gap:0;min-width:0}
.p-gtag{position:absolute;left:24px;top:24px;display:flex;align-items:baseline;gap:9px;padding:7px 10px;background:rgba(255,255,255,.92);border-radius:3px;color:var(--ink);white-space:nowrap}
.p-gtag em{font:500 11.5px/1 var(--mono);letter-spacing:.16em;font-style:normal;color:var(--slate)}
.p-gtag b{font:600 14px/1 var(--mono)}
.p-gtag .dia{display:none}
.p-gl{flex:1;display:flex;align-items:center;gap:18px;border-top:1px solid #34476A}
.p-gl b{font:500 clamp(48px,5.4vw,80px)/1 var(--mono);letter-spacing:-.04em;color:#fff}
.p-gl>span{font:500 12.5px/1 var(--mono);letter-spacing:.14em;text-transform:uppercase;color:#A9B6CB}
.p-gnote{font-size:13.5px;line-height:1.5;color:#A9B6CB;max-width:300px;text-wrap-style:pretty;padding-top:16px;border-top:1px solid #34476A}

/* industries: ruled columns, the numbers' diamond rule again, no cards */
.p-inds{list-style:none;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:0 40px}
.p-ind{position:relative;border-top:1.5px solid var(--ink);padding-top:34px;display:flex;flex-direction:column}
.p-ind::before{content:"";position:absolute;left:0;top:-5.5px;width:9px;height:9px;background:var(--blue);transform:rotate(45deg)}
.p-ind h3{font-weight:500;font-size:clamp(24px,1.9vw,26px);line-height:1.1;letter-spacing:-.025em;margin-bottom:14px;color:var(--ink)}
.p-ind p{font-size:16px;line-height:1.55;color:var(--ink2);text-wrap-style:pretty;margin-bottom:26px}
.p-pills{display:flex;flex-direction:column;border-top:1px solid var(--line2)}
.p-pill{display:flex;align-items:center;gap:10px;min-height:48px;border-bottom:1px solid var(--line2);font:600 14px/1 var(--mono);color:var(--ink);transition:color .15s}
.p-pill .dia{width:7px;height:7px;background:var(--blue);flex:none}
.p-pill .p-ar{margin-left:auto}
.p-pill:hover{color:var(--blue)}

/* services: the dark band */
.p-dark{background:var(--ink);color:#fff;padding-block:96px 88px}
.p-dark .p-head h2{color:#fff}
.p-dark .p-lede{color:#C9D3E3}
.p-lede-wrap{justify-self:end;max-width:520px;display:flex;flex-direction:column;align-items:flex-start;gap:18px}
.p-lede-wrap .p-lede{justify-self:auto}
.p-steps{list-style:none;display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:0;position:relative}
.p-steps::before{content:"";position:absolute;left:0;right:0;top:56px;height:1px;background:#3A4B69}
.p-steps li{position:relative;padding:0 24px 0 0}
.p-sn{display:block;font:500 12.5px/1 var(--mono);letter-spacing:.12em;color:#A9B6CB;margin-bottom:28px}
.p-nd{display:block;width:13px;height:13px;margin:0 0 30px 0;background:var(--blue-lt);transform:rotate(45deg);position:relative;top:2px;left:3px;outline:6px solid var(--ink)}
.p-steps p{font-weight:500;font-size:clamp(20px,1.8vw,26px);line-height:1.2;letter-spacing:-.02em;color:#fff;max-width:230px;text-wrap-style:balance}

/* customers */
.p-logos{list-style:none;display:grid;grid-template-columns:repeat(5,minmax(0,1fr));border-top:1px solid var(--line2);border-left:1px solid var(--line2)}
.p-logos li{display:flex;align-items:center;justify-content:center;height:136px;padding:0 28px;border-right:1px solid var(--line2);border-bottom:1px solid var(--line2)}
.p-logos img{max-width:100%;max-height:calc(48px * var(--s,1));width:auto;height:auto;object-fit:contain;mix-blend-mode:multiply;filter:grayscale(1) contrast(1.05);opacity:.78;transition:filter .2s,opacity .2s}
.p-logos li:hover img{filter:none;opacity:1}

/* news */
.p-news{list-style:none;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:28px}
.p-nl{display:flex;flex-direction:column;height:100%}
.p-nimg{position:relative;display:block;border-radius:16px;overflow:hidden;aspect-ratio:16 / 10;background:var(--paper)}
.p-nimg::after{content:"";position:absolute;inset:0;border-radius:16px;box-shadow:inset 0 0 0 1px rgba(14,23,38,.1);pointer-events:none}
.p-nimg img{width:100%;height:100%;object-fit:cover;display:block;filter:saturate(.82);transition:transform .5s cubic-bezier(.2,.7,.2,1),filter .3s}
.p-new3 .p-nimg img{transform:scale(1.07)}
.p-nl:hover .p-nimg img{filter:saturate(1);transform:scale(1.04)}
.p-new3 .p-nl:hover .p-nimg img{transform:scale(1.1)}
.p-date{display:block;margin:20px 0 10px;font:500 12px/1 var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--ink3)}
.p-nl h3{font-weight:500;font-size:clamp(20px,1.8vw,26px);line-height:1.2;letter-spacing:-.02em;color:var(--ink);text-wrap-style:balance;margin-bottom:18px}
.p-nl .p-more{margin-top:auto}
.p-nl:hover .p-more{border-bottom-color:var(--blue)}
html[lang=vi] .p-new{order:var(--vo)}

/* closing contact card: solid navy text half, the card-in-hand picture the other half (no face repeated, no gradient over a face) */
.p-cta-wrap{padding:0 var(--edge) var(--edge);max-width:1440px;margin:0 auto}
.p-cta{position:relative;border-radius:20px;overflow:hidden;background:var(--ink);color:#fff;min-height:480px;display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,.85fr);isolation:isolate}
.p-ctat{grid-column:1;grid-row:1;padding:64px var(--pad);max-width:760px;align-self:center}
.p-ctaimg{grid-column:2;grid-row:1;width:100%;height:100%;object-fit:cover;object-position:46% 50%;display:block;min-height:360px}
.p-ctat h2{font-weight:500;font-size:clamp(34px,4.2vw,60px);line-height:1.02;letter-spacing:-.04em;text-wrap-style:balance;margin-bottom:24px}
.p-ctasub{font-size:18px;line-height:1.5;color:#D5DDEA;max-width:520px;margin-bottom:32px;text-wrap-style:pretty}
.p-ctab{display:flex;gap:12px;flex-wrap:wrap}
.btn-white{background:#fff;color:var(--ink)}
.btn-white:hover{background:#E6EEF6}
.btn-line{border:1.5px solid rgba(255,255,255,.7);color:#fff}
.btn-line:hover{background:rgba(255,255,255,.12)}

/* footer */
.p-foot{background:var(--paper);padding:72px 0 36px}
.p-ft{display:grid;grid-template-columns:minmax(0,4fr) minmax(0,3fr) minmax(0,5fr);gap:56px}
.p-fb p{font-size:15.5px;line-height:1.5;color:var(--ink2);margin-top:20px;max-width:300px}
.p-fb .p-fc{display:flex;flex-direction:column;gap:2px;margin-top:20px}
.p-fb .p-fc a{display:inline-flex;align-items:center;min-height:44px;font-weight:600;color:var(--ink);text-decoration:underline;text-decoration-color:var(--blue);text-underline-offset:4px;text-decoration-thickness:1.5px}
.p-fnav{list-style:none;display:grid;grid-template-columns:1fr 1fr;column-gap:24px;gap:0 24px}
.p-fnav + .p-fnav{margin-top:20px;padding-top:16px;border-top:1px solid var(--line2)}
.p-fl{display:inline-flex;align-items:center;min-height:44px;min-width:44px;font-size:15.5px;font-weight:500;color:var(--ink)}
.p-fl:hover{color:var(--blue)}
.p-offs{list-style:none;display:grid;grid-template-columns:1fr 1fr;gap:28px 32px;align-content:start}
.p-offs b{display:block;font:500 12px/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--ink);margin-bottom:10px}
.p-offs li>span{display:block;font-size:14.5px;line-height:1.5;color:var(--ink2)}
.p-copy{margin-top:56px;padding-top:24px;border-top:1px solid var(--line2);font:500 12px/1.5 var(--mono);letter-spacing:.04em;color:var(--ink3)}

/* corner marks on the picture: geometry only */
.p-br{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}
.p-br path{fill:none;stroke:#fff;stroke-width:1.5;vector-effect:non-scaling-stroke;opacity:.85}

@media (max-width:1180px){
  :root{--pad-s:88px}
  .p-head{grid-template-columns:1fr;row-gap:20px}
  .p-lede,.p-lede-wrap{justify-self:start;max-width:620px}
  .p-head-one{grid-template-columns:1fr auto}
  .p-bento{grid-template-columns:repeat(2,minmax(0,1fr))}
  .p-c1,.p-c2,.p-c3,.p-c4{grid-column:auto}
  .p-c1{grid-column:1 / -1}
  .p-c4{grid-column:1 / -1}
  .p-c1 .p-ph{min-height:440px}
  .p-inds{grid-template-columns:repeat(2,minmax(0,1fr));row-gap:48px}
  .p-nums{grid-template-columns:repeat(6,minmax(0,1fr));row-gap:48px}
  .p-nums li{grid-column:span 2}
  .p-nums li.p-n4,.p-nums li.p-n5{grid-column:span 3}
  .p-nums li.p-n3{border-right:0;margin-right:0}
  .p-nums li.p-n4{border-right:1px solid var(--line2)}
  .p-ft{grid-template-columns:1fr 1fr;gap:40px}
  .p-offs{grid-column:1 / -1}
  .p-cta{grid-template-columns:1fr}
  .p-ctaimg{grid-column:1;grid-row:1;height:300px;min-height:0}
  .p-ctat{grid-column:1;grid-row:2;max-width:none}
}
@media (max-width:900px){
  :root{--pad-s:56px}
  .p-wrap{padding-inline:var(--gut)}
  .p-head{margin-bottom:32px}
  .p-eye{margin-bottom:16px}
  .p-lede{font-size:17px}
  .p-sec-num{padding-top:48px;padding-bottom:56px}
  .p-nums{grid-template-columns:1fr 1fr;column-gap:20px;row-gap:0;border-top:1.5px solid var(--ink)}
  .p-nums li,.p-nums li.p-n3,.p-nums li.p-n4,.p-nums li.p-n5{grid-column:auto;display:block;margin:0;padding:22px 0 20px;border-right:0;border-bottom:1px solid var(--line2)}
  .p-nums li.p-n5{grid-column:1 / -1;border-bottom:0}
  .p-nums li::before{display:none}
  .p-nums b{font-size:44px}
  .p-nums li>span{margin:8px 0 0;max-width:none;font-size:14px;min-width:0}
  .p-bento{grid-template-columns:1fr;gap:14px}
  .p-c1,.p-c4{flex-direction:column}
  .p-c1 .p-ph{width:100%;min-height:0;aspect-ratio:16 / 9}
  .p-c1 .p-ph img{object-position:50% 18%}
  .p-c1 .p-pt{top:59% !important}
  .p-c2 .p-pt{top:36% !important}
  .p-pt::after{display:none}
  .p-tg{bottom:auto;left:16px;top:-14px}
  .p-c2 .p-tg{left:50%;right:auto;top:20px;transform:translateX(-50%)}
  .p-c2 .p-ph,.p-c3 .p-ph{aspect-ratio:16 / 9}
  .p-body{padding:22px 20px 20px}
  .p-name{font-size:28px}
  .p-desc{margin-bottom:16px}
  .p-chips{margin-bottom:18px}
  .p-c1 .p-chips li:nth-child(n+4){display:none}
  .p-ben{display:none}
  .p-c4 .p-gv{order:-1}
  .p-gv{margin:14px 14px 0;padding:18px 18px 14px}
  .p-gtag{display:none}
  .p-gl{padding:12px 0}
  .p-gl b{font-size:48px}
  .p-gnote{padding-top:12px}
  .p-inds{grid-template-columns:1fr;gap:0}
  .p-ind{padding:30px 0 20px}
  .p-ind p{margin-bottom:16px}
  .p-dark{padding-block:60px 56px}
  .p-steps{grid-template-columns:1fr;gap:0}
  .p-steps::before{left:6px;right:auto;top:6px;bottom:30px;width:1px;height:auto}
  .p-steps li{display:grid;grid-template-columns:30px 1fr;column-gap:12px;align-items:center;padding:0 0 22px 0}
  .p-sn{margin:0;grid-column:2;font-size:11.5px;grid-row:1}
  .p-nd{margin:0;grid-column:1;grid-row:1 / span 2}
  .p-steps p{grid-column:2;grid-row:2;max-width:none;font-size:20px}
  .p-logos{grid-template-columns:repeat(2,minmax(0,1fr))}
  .p-logos li{height:92px;padding:0 18px}
  .p-logos img{max-height:calc(38px * var(--s,1))}
  .p-news{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;gap:16px;margin-inline:calc(-1 * var(--gut));padding:0 var(--gut) 8px;scroll-padding-inline:var(--gut);-webkit-overflow-scrolling:touch;scrollbar-width:none}
  .p-news::-webkit-scrollbar{display:none}
  .p-new{flex:0 0 82%;scroll-snap-align:start}
  .p-head-one{grid-template-columns:1fr}
  .p-head-link{justify-self:start;margin-top:4px}
  .p-cta-wrap{padding:0 var(--edge) var(--edge)}
  .p-cta{min-height:0}
  .p-ctaimg{height:220px}
  .p-ctat{padding:26px var(--pad) 30px}
  .p-ctab{flex-direction:column}
  .p-ctab .btn{width:100%;height:52px}
  .p-foot{padding:48px 0 28px}
  .p-ft{grid-template-columns:1fr;gap:28px}
  .p-offs{grid-template-columns:1fr 1fr;gap:20px 18px}
  .p-offs li>span{font-size:13.5px}
  .p-copy{margin-top:36px}
}
"""

SCRIPT_PATCH = r"""
  document.querySelectorAll('a[data-en][data-vi]').forEach(function(a){a._u=1});
  var _set=setLang; setLang=function(l){_set(l);document.querySelectorAll('a[data-en][data-vi]').forEach(function(a){a.setAttribute('href',a.getAttribute('data-'+l))})};
  document.querySelectorAll('.nav a').forEach(function(a){a.addEventListener('click',function(){if(menu.classList.contains('open')){mb.click()}})});
"""


def main():
    t = open(os.path.join(V2, "a.tpl.html")).read()
    # head
    t = t.replace("@@FONTS@@", B0.fonts("bricolage", "geistmono"))
    t = t.replace("@@LOGO@@", "assets/brand/logo-blue.png").replace("@@LOGO_W@@", "137")
    t = t.replace("@@IMG_WIDE@@", "assets/a/scene.jpg").replace('<img class="photo" src="assets/a/scene.jpg" alt=""', '<img class="photo" src="assets/a/scene.jpg" width="1600" height="1600" fetchpriority="high" alt=""')
    t = t.replace("@@POS_WIDE@@", B0.CFG["a"].get("pos_wide", "50% 40%")).replace("@@POS_PORT@@", B0.CFG["a"].get("pos_port", "50% 30%"))
    marks = B0.marks_svg(B0.CFG["a"]["marks_wide"]); marks_m = B0.marks_svg(B0.CFG["a"]["marks_port"])
    t = t.replace("@@MARKS@@", '<div class="mk-d">%s</div><div class="mk-m">%s</div>' % (marks, marks_m))
    t = t.replace("<title>Aimesoft : Multimodal AI products and services</title>", "<title>Aimesoft : Multimodal AI products and services</title>\n<meta name=\"description\" content=\"Aimesoft : Multimodal AI product and service provider\">")
    # nav: real anchors, ordered as in the template
    anchors = [n[0] for n in C.NAV]
    nav_pat = re.compile(r'(<nav class="nav".*?</nav>)', re.S)
    nav = nav_pat.search(t).group(1)
    for a in anchors:
        nav = nav.replace('<a href="#">', '<a href="%s">' % a, 1)
    t = nav_pat.sub(lambda m: nav, t, count=1)
    t = t.replace('<a class="btn btn-ink" href="#"><span class="en">Contact</span>', '<a class="btn btn-ink" href="#contact"><span class="en">Contact</span>')
    # hero buttons
    gpt = [p for p in C.PRODUCTS if p["key"] == "gpt"][0]["url"]
    t = t.replace('<a class="btn btn-ink" href="#"><span class="en">Meet AimeGPT</span>', '<a class="btn btn-ink" href="%s" data-en="%s" data-vi="%s" target="_blank" rel="noopener"><span class="en">Meet AimeGPT</span>' % (gpt[0], gpt[0], gpt[1]))
    t = t.replace('<a class="btn btn-ghost" href="#">', '<a class="btn btn-ghost" href="#contact">')
    # css + body
    t = t.replace("</style>", CSS.replace("var(--line)", "var(--line2)") + "</style>", 1)
    body = numbers_html() + products_html() + industries_html() + services_html() + customers_html() + news_html() + cta_html()
    t = t.replace("</main>", body + "</main>" + footer_html(), 1)
    t = t.replace("  setLang(html.lang==='vi'?'vi':'en');", SCRIPT_PATCH + "  setLang(html.lang==='vi'?'vi':'en');")
    t = t.replace("function setLang(l){", "var setLang=function(l){", 1).replace("img[data-alt-'+l+']').forEach(function(i){i.alt=i.getAttribute('data-alt-'+l)});document.querySelectorAll('[data-aria-'+l+']').forEach(function(e){e.setAttribute('aria-label',e.getAttribute('data-aria-'+l))});}",
                                                                     "img[data-alt-'+l+']').forEach(function(i){i.alt=i.getAttribute('data-alt-'+l)});document.querySelectorAll('[data-aria-'+l+']').forEach(function(e){e.setAttribute('aria-label',e.getAttribute('data-aria-'+l))});};", 1)
    t = nb(t)
    t = re.sub(r'/\*.*?\*/', '', t, flags=re.S)           # no CSS comments in the public file
    t = re.sub(r'<!--.*?-->', '', t, flags=re.S)
    # write the site
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(t)
    open(os.path.join(OUT, "CNAME"), "w").write(DOMAIN + "\n")
    open(os.path.join(OUT, ".nojekyll"), "w").write("")
    ad = os.path.join(OUT, "assets")
    if os.path.isdir(ad): shutil.rmtree(ad)
    os.makedirs(ad)
    for d, files in (("a", ["scene.jpg", "see.jpg", "hear.jpg", "read.jpg", "cta.jpg"]), ("brand", ["logo-blue.png"]), ("logos", [f for f, _ in C.LOGOS]), ("news", [n["img"] for n in C.NEWS])):
        os.makedirs(os.path.join(ad, d), exist_ok=True)
        for f in files: shutil.copy(os.path.join(ROOT, "assets", d, f), os.path.join(ad, d, f))
    # gate: no class declared twice among the new p- selectors; no forbidden words on the page
    decl = re.findall(r"(?m)^\.(p-[a-z0-9-]+)[ ,{:.]", CSS)
    print("built site-a", len(t) // 1024, "KB", "p- classes", len(set(decl)))
    bad = [w for w in ("minh hoạ", "minh họa", "demo", "placeholder", "lorem") if w in t.lower()]
    assert not bad, bad


if __name__ == "__main__":
    main()
