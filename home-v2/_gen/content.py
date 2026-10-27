#!/usr/bin/env python3
"""Shared content for the two Aimesoft 2.0 home pages (A light, B dark).
Every fact here is traceable to a page on aimesoft.com (EN) or aimesoft.com/vi/ (VI), read 27/10/2026.
VI strings are copied from the live VI site; where the VI site has no equivalent the string is a short UI label.
Source page is noted next to each block so a reviewer can open it.
"""
SITE = "https://www.aimesoft.com"
VERSION = "0.1.0"


def bi(en, vi):
    """Bilingual pair. CSS shows one by html[lang]."""
    return '<span class="en">%s</span><span class="vi">%s</span>' % (en, vi)


def link(path_en, path_vi=None):
    """Absolute link to the live site, EN and VI. Returns (en_url, vi_url)."""
    return (SITE + path_en, SITE + "/vi" + (path_vi or path_en))


# ---------------------------------------------------------------- nav
NAV = [  # (anchor, EN, VI)
    ("#multimodal", "Multimodal AI", "Multimodal AI"),
    ("#products", "Products", "Sản phẩm"),
    ("#services", "Services", "Dịch vụ"),
    ("#customers", "Customers", "Khách hàng"),
    ("#news", "News", "Tin tức"),
]

# ---------------------------------------------------------------- multimodal lede (home page intro, both languages)
MM_EN = "Multimodal AI combines multiple input sources (text, voice, image, numerical data, etc) and various intelligence algorithms into a single system to solve complicated problems and achieve high performance."
MM_VI = "Trí tuệ nhân tạo đa thể thức là một loại trí tuệ nhân tạo trong đó nhiều nguồn dữ liệu (văn bản, tiếng nói, ảnh, số liệu) và nhiều thuật toán xử lý thông minh được kết hợp lại để giải quyết các bài toán phức tạp và đạt được độ chính xác cao hơn."

# ---------------------------------------------------------------- numbers (each one printed on aimesoft.com)
NUMBERS = [
    # big, EN caption, VI caption, source page
    ("200+", "installations worldwide", "lượt triển khai trên toàn cầu", "home page h1 (the company page says 300+ in another sentence; the site contradicts itself, only 200+ is used)"),
    ("2018", "Aimesoft established", "Aimesoft được thành lập", "company page"),
    ("99%+", "character-level accuracy of AimeCard OCR", "độ chính xác của AimeCard khi nhận diện chữ in", "aimecard page"),
    ("40+", "languages supported by AimeTalk presentations", "ngôn ngữ AimeTalk hỗ trợ khi thuyết trình", "products page"),
    ("Top 10", "Map of AI Platform and Application Development 2025", "Bản đồ Doanh nghiệp Cung cấp nền tảng, Phát triển ứng dụng AI 2025", "company page, press 15/10/2025"),
]

# ---------------------------------------------------------------- products (SEE / HEAR / READ / LANGUAGE)
PRODUCTS = [
    dict(key="face", verb=("SEE", "NHÌN"), name="AimeFace", url=link("/aimeface.html"),
         line=("eKYC, face recognition solution", "Nhận diện khuôn mặt, nhận diện khách hàng, eKYC"),
         desc=("AimeFace is an eKYC (know your customer), face recognition, face registration solution from Aimesoft.",
               "AimeFace là giải pháp nhận biết khách hàng của bạn (eKYC) thông qua công nghệ nhận dạng khuôn mặt, đăng ký khuôn mặt được phát triển bởi Aimesoft."),
         chips=[("Real-time face recognition, detection, and identification", "Nhận diện khuôn mặt Real-time"),
                ("Comparison between actual faces and face images in ID cards", "So sánh giữa khuôn mặt thực tế và hình ảnh khuôn mặt trong thẻ ID")]),
    dict(key="speech", verb=("HEAR", "NGHE"), name="AimeSpeech", url=link("/aimespeech.html"),
         line=("Speech recognition (STT), speech synthesis (TTS), Speaker identification", "Nhận dạng tiếng nói, nhận diện người nói, tổng hợp tiếng nói"),
         desc=("AimeSpeech is a core speech processing framework inside the Aimenicorn software ecosystem.",
               "AimeSpeech là nền tảng về xử lý giọng nói bên trong hệ sinh thái phần mềm trí tuệ nhân tạo đa thể thức Aimenicorn."),
         chips=[("Speech recognition (Speech-to-Text, STT)", "Nhận dạng giọng nói (Chuyển tiếng nói thành văn bản, STT, ASR)"),
                ("Speech Synthesis (Text-to-Speech, TTS)", "Tổng hợp tiếng nói (Chuyển văn bản thành giọng nói, TTS)")]),
    dict(key="card", verb=("READ", "ĐỌC"), name="AimeCard", url=link("/aimecard.html"),
         line=("Universal OCR platform", "Số hoá, OCR, nhận diện chứng minh thư, hộ chiếu, bằng lái xe"),
         desc=("AimeCard is a universal OCR platform for optical character recognition in the Aimenicorn software ecosystem.",
               "AimeCard là sản phẩm Intelligence OCR (optical character recognition, nhận diện chữ viết) của Aimesoft."),
         chips=[("Driving license and passport recognition", "Phân tích được cấu trúc của văn bản"),
                ("Invoices and documents recognition", "Nhận diện được nhiều loại văn bản khác nhau, hỗ trợ đa ngôn ngữ")]),
    dict(key="gpt", verb=("LANGUAGE", "NGÔN NGỮ"), name="AimeGPT", url=link("/aimegpt.html"),
         line=("Private instruction following GPT, mini-ChatGPT", "Mô hình GPT, mini-chatgpt tuân theo hướng dẫn"),
         desc=("AimeGPT is a series of GPT-2 (Generative Pre-trained Transformer), GPT-3, instruction following GPT-3, mini-ChatGPT models from Aimesoft. We provide the GPT models for Japanese and Vietnamese.",
               "AimeGPT là một loạt các mô hình GPT-2, GPT-3, GPT-3 theo hướng chỉ dẫn, mini-ChatGPT của Aimesoft. Chúng tôi cung cấp các mô hình GPT trên tiếng Nhật, tiếng Việt."),
         chips=[("On-premise deployment", "Triển khai trên server khách hàng"),
                ("Fine-tuning with domain data", "Tinh chỉnh trên miền dữ liệu cụ thể")]),
]
PRODUCTS_ALL = link("/products.html")
LEARN = ("Learn more", "Xem thêm")

# ---------------------------------------------------------------- industries (the site has no industry page; the home page names
# "Healthcare, Hospitality, Transportation" and the product pages name the rest. Each tile cites a product page.)
INDUSTRIES_LEDE = (
    "At Aimesoft, we provide end-to-end Multimodal AI integrated solutions across a wide range of industries such as Healthcare, Hospitality, Transportation, etc.",
    "Tại Aimesoft, chúng tôi cung cấp trọn gói các giải pháp tích hợp trí tuệ nhân tạo đa thể thức cho nhiều ngành công nghiệp như Chăm sóc sức khỏe, Khách sạn, Vận tải,...",  # aimesoft.com/vi/services.html
)
SERVICES_LEDE = ("In addition to developing AI-powered products, we provide consulting services to enable companies to understand, evaluate and adopt Artificial Intelligence.", "Ngoài việc phát triển các sản phẩm hỗ trợ bằng AI, chúng tôi cung cấp dịch vụ tư vấn để các công ty hiểu, đánh giá và áp dụng Trí tuệ nhân tạo.")  # EN: home page; VI: aimesoft.com/vi/services.html
INDUSTRIES = [
    dict(name=("Hospitality", "Khách sạn"), products=[("AimeHotel", link("/aimehotel.html")), ("AimeReception", link("/aimereception.html"))],
         line=("Virtual hotel clerk and virtual receptionist that welcome guests and offer information.",
               "Nhân viên khách sạn ảo và lễ tân ảo chào đón khách, cung cấp thông tin.")),
    dict(name=("Healthcare", "Chăm sóc sức khỏe"), products=[("AimeHospital", link("/aimehospital.html"))],
         line=("A smart healthcare solution that can analyze medical records using Multimodal AI.",
               "Giải pháp chăm sóc sức khỏe thông minh, phân tích bệnh án dựa trên Trí tuệ nhân tạo đa thể thức.")),
    dict(name=("Retail", "Bán lẻ"), products=[("Aime AIShop", link("/aimeaishop.html"))],
         line=("Recognizes images, voices, and languages to support customers in retail stores or supermarkets.",
               "Tự động nhận diện hình ảnh, tiếng nói, ngôn ngữ để hỗ trợ khách hàng trong cửa hàng hoặc siêu thị.")),
    dict(name=("Customer service", "Chăm sóc khách hàng"), products=[("AimeFluent", link("/aimefluent.html"))],
         line=("Automated customer service for consulting, finance - banking, education, tourism, e-commerce, law.",
               "Chăm sóc khách hàng tự động: tư vấn, tài chính - ngân hàng, giáo dục, du lịch, thương mại điện tử, pháp luật.")),
]

# ---------------------------------------------------------------- services (home page "Our End-to-End AI Services")
SERVICES_H = ("Our End-to-End AI Services", "Dịch vụ AI toàn diện")
STEPS = [
    ("Discover and understand the insights", "Khai phá và thấu hiểu"),
    ("Consult (Give advisory)", "Tư vấn (Đưa ra lời khuyên)"),
    ("PoC (Solutions and Analysis)", "PoC (Giải pháp và phân tích)"),
    ("Production", "Triển khai"),
    ("Evaluation & Support", "Đánh giá & Hỗ trợ"),
]
SERVICES_MORE = link("/services.html")

# ---------------------------------------------------------------- customers: the ten logos on the home page, in page order
# (file, name as printed in the logo or the page alt text)
LOGOS = [
    ("tokushukai.png", "Tokushukai Information System"),
    ("dentsu.png", "Dentsu Digital"),
    ("nexus.png", "Nexus Frontiertech"),
    ("jcm.png", "JCM Global"),
    ("tng.png", "TNG"),
    ("rath.png", "RATH"),
    ("ninehours.png", "nine hours"),
    ("markitone.png", "MarkitOne"),
    ("fine.png", "Fine Japan"),
    ("prominent.png", "Prominent"),
]

CLIENTS_H = ("Our clients", "Khách hàng tiêu biểu")  # home page h2, EN and VI

# ---------------------------------------------------------------- news: three newest on the home page and press page
NEWS = [
    dict(img="dxpo.jpg", date=("Aug 10, 2026", "10/08/2026"), url=link("/press_dxpo_20260811.html"),
         title=("Aimesoft Exhibiting at Manufacturing Innovation DXPO Tokyo Summer 2026",
                "Aimesoft tham gia triển lãm Manufacturing Innovation DXPO Tokyo Hè 2026"), vi_order=1),
    dict(img="viie.jpg", date=("Oct 24, 2025", "29/09/2025"), url=link("/press_viie2025_20250929.html"),
         title=("Aimesoft to Showcase Multimodal AI Solutions at Vietnam International Innovation Expo 2025",
                "Aimesoft tham gia Triển lãm quốc tế Đổi mới sáng tạo Việt Nam 2025 (VIIE 2025) - Đón đầu xu hướng Multimodal AI"), vi_order=3),
    dict(img="top10.jpg", date=("Oct 15, 2025", "13/10/2025"), url=link("/press_top10_2025_20251013.html"),
         title=("Aimesoft JSC Honored in the Top 10 on the Map of AI Platform and Application Development 2025 (Vietnam Tech & Map 2025 Award)",
                "Aimesoft vinh dự đạt danh hiệu Top 10 trên Bản đồ Doanh nghiệp Cung cấp nền tảng, Phát triển ứng dụng AI 2025"), vi_order=2),
]
NEWS_ALL = link("/press.html")
NEWS_H = ("News & Blog", "Tin tức và Blog")

# ---------------------------------------------------------------- contact + footer (home page footer, company page)
CTA_H = ("Transform your business with the power of Multimodal AI", "Transform your business with the power of Multimodal AI")  # VI home keeps this line in English
CTA_SUB = ("Call (855) 302 8668 for a free consultation, or write to info@aimesoft.com.",
           "Gọi +84 98-538-7426 hoặc gửi email tới info@aimesoft.com.")
PHONE = ("(855) 302 8668", "+84 98-538-7426")
PHONE_TEL = ("tel:+18553028668", "tel:+84985387426")
EMAIL = "info@aimesoft.com"
CONTACT_URL = link("/contact.html")
OFFICES = [  # (name EN, name VI, address EN, address VI); the VI site prints San Jose and Tokyo in English, Hanoi and the south in Vietnamese
    ("San Jose", "San Jose", "2150 Ringwood Ave., San Jose, California 95131, USA", "2150 Ringwood Ave., San Jose, California 95131, USA"),
    ("Tokyo", "Tokyo", "3F, Shiodome Bldg., 1-2-20 Kaigan, Minato-ku, Tokyo 105-0022, Japan", "3F, Shiodome Bldg., 1-2-20 Kaigan, Minato-ku, Tokyo 105-0022, Japan"),
    ("Hanoi", "Hà Nội", "10F, Viet A Tower, 9 Duy Tan Street, Cau Giay, Hanoi, Vietnam", "Tầng 10, Toà nhà Việt Á Tower, Số 9 phố Duy Tân, Cầu Giấy, Hà Nội"),
    ("Southern Vietnam", "Miền Nam", "SAV2-01.05 The Sun Avenue, No.28 Mai Chi Tho Str., An Phu Ward, Thu Duc City, HCMC, Vietnam", "SAV2-01.05 The Sun Avenue, Số 28 Mai Chí Thọ, An Phú, Thủ Đức, TP. Hồ Chí Minh"),
]
FOOT_LINKS = [
    (("Solution", "Giải pháp"), link("/products.html")),
    (("Service", "Dịch vụ"), link("/services.html")),
    (("Technology", "Công nghệ"), link("/multimodalai.html")),
    (("Career", "Tuyển dụng"), link("/jobs.html")),
    (("News", "Tin tức"), link("/press.html")),
    (("Contact Us", "Liên hệ"), link("/contact.html")),
    (("Privacy Policy", "Chính sách bảo mật"), link("/privacy.html")),
]
SOCIAL = [("Facebook", "https://www.facebook.com/aimesoft"), ("X", "https://twitter.com/aimesoftinc"), ("LinkedIn", "https://www.linkedin.com/company/aimesoft")]
TAGLINE = ("Multimodal AI software product and service provider", "Nghiên cứu, phát triển, phân phối và cung cấp dịch vụ liên quan đến phần mềm Trí tuệ nhân tạo đa thể thức")  # company page "What we do" / "Hoạt động"
COPY = "Copyright © 2018 - 2026 Aimesoft. All Rights Reserved."
