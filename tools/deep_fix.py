#!/usr/bin/env python3
"""Deep audit fixes for Ha Tinh showcase."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT.parent / "template-scrapes"
IMG = "../assets/shared-images"
FORM = 'onsubmit="event.preventDefault();alert(\'Demo — form chưa kết nối backend.\');return false;"'


def p(name: str) -> str:
    return f"{IMG}/{name}"


def fix_forms(html: str) -> str:
    def repl(m: re.Match) -> str:
        tag = m.group(0)
        return tag if "onsubmit=" in tag else tag[:-1] + f" {FORM}>"
    return re.sub(r"<form\b[^>]*>", repl, html, flags=re.I)


def strip_vendor_links(html: str) -> str:
    html = re.sub(r'href="https?://[^"]*(?:webflow\.com|flowcub|colorlib|duruthemes|max-themes)[^"]*"', 'href="#"', html, flags=re.I)
    html = re.sub(r'href="http://www\.(facebook|twitter|youtube|google|linkedin)\.com/"', 'href="#"', html)
    return html


# --- TRAVOL ---
TRAVOL_NAV = """                <ul class="navbar-nav ms-auto">
                    <li class="nav-item"><a class="nav-link{home}" href="index.html">Trang chủ</a></li>
                    <li class="nav-item"><a class="nav-link{about}" href="about.html">Giới thiệu</a></li>
                    <li class="nav-item"><a class="nav-link{tours}" href="tours.html">Tour</a></li>
                    <li class="nav-item"><a class="nav-link{dest}" href="destination.html">Điểm đến</a></li>
                    <li class="nav-item"><a class="nav-link{gallery}" href="gallery.html">Gallery</a></li>
                    <li class="nav-item"><a class="nav-link{contact}" href="contact.html">Liên hệ</a></li>
                </ul>"""

LOGO = '<a class="logo" href="index.html"><h2 style="color:#fff;margin:0;font-size:22px">HA TINH <span style="color:#e9a225">Travel</span></h2></a>'


TRAVOL_REPL = [
    (", Europe", ", Hà Tĩnh"),
    ("Europe,", "Hà Tĩnh,"),
    (" Ven biển, Hà Tĩnh", " Ven biển Hà Tĩnh"),
    ("Hương Tích, Hà Tĩnh", "Chùa Hương Tích"),
    ("Perugia", "Hương Tích"),
    ("Travel dapibus", "Hành trình"),
    ("Samantha Brown", "Nguyễn Thu Hà"),
    ("Olivia Martin", "Trần Minh Anh"),
    ("Nolan White", "Lê Văn Đức"),
    ("Leonie Norman", "Nguyễn Thu Hà"),
    ("Andreas Brown", "Trần Minh Anh"),
    ("Angelina White", "Lê Thị Lan"),
    ("Emily Norman", "Nguyễn Thu Hà"),
    ("Emily Brown", "Nguyễn Thu Hà"),
    ("Switzerland Guide", "Hướng dẫn viên"),
    ("Thiên Cầm Guide", "Hướng dẫn Thiên Cầm"),
    ("Kẻ Gỗ Guide", "Hướng dẫn Kẻ Gỗ"),
    ("info@travolagency.com", "contact@hatinhtravel.demo"),
    ("info@luxuryhotel.com", "contact@hatinhtravel.demo"),
    ('<span class="">Discover</span> the world with our guide', "Khám phá Hà Tĩnh cùng hướng dẫn viên địa phương"),
    ("We helping you find <span>your dream</span> vacation", "Đồng hành cùng bạn <span>khám phá</span> Hà Tĩnh"),
    ("Travel Experts", "Đội ngũ chuyên gia"),
    ("Meet Our <span>Guides</span>", "Gặp gỡ <span>hướng dẫn viên</span>"),
    ("Top Destination", "Điểm đến nổi bật"),
    ("Popular <span>Destination</span>", "Điểm đến <span>phổ biến</span>"),
    ("Choose your destination", "Chọn điểm đến"),
    ("Most Popular", "Được yêu thích"),
    ("<span>Travel</span> Countries", "<span>Vùng</span> miền"),
    ("<span>Travel Blog</span>", "<span>Blog</span> du lịch"),
    ("<span>Travel</span> Experience", "<span>Kinh nghiệm</span> du lịch"),
    ("Flight Booking", "Lịch tour đã tổ chức"),
    ("Amazing Tour", "Tour đa dạng"),
    ("Cruises Booking", "Tour ven biển"),
    ("Ticket Booking", "Vé tham quan"),
    ("Costa Victoria Cochin", "Tour khám phá Thiên Cầm"),
    ("4 Days + 3 Nights", "4 ngày 3 đêm"),
    ("4+ Tour Packages", "4+ gói tour"),
    ("3+ Tour Packages", "3+ gói tour"),
    ("6+ Tour Packages", "6+ gói tour"),
    ("7+ Tour Packages", "7+ gói tour"),
    ("Images and Videos", "Hình ảnh & video"),
    ("Image <span>&amp;</span> Video <span>Gallery</span>", "Thư viện <span>ảnh</span> & <span>video</span>"),
    ("Images", "Hình ảnh"),
    ("Image <span>Gallery</span>", "Thư viện <span>ảnh</span>"),
    ("Videos", "Video"),
    ("Video <span>Gallery</span>", "Thư viện <span>video</span>"),
    ("Liên hệ <span>Us</span>", "Liên hệ"),
    ("Travel Agency Inc.", "Ha Tinh Travel"),
    ("Travel Agency", "Công ty du lịch"),
    (
        "Travel duru nisl quam nestibulum ac quam nec odio elementum sceisue the aucan ligula. Orci varius natoque penatibus et magnis dis parturient monte nascete ridiculus mus nellentesque habitant morbine.",
        "Chúng tôi tư vấn tour biển, hồ Kẻ Gỗ, chùa Hương Tích và các điểm di tích lịch sử tại Hà Tĩnh — phù hợp gia đình, nhóm bạn và khách muốn trải nghiệm chậm rãi.",
    ),
    (
        "Agency elementum sesue the aucan vestibulum aliquam justo in sapien rutin volutpat. Donec in quis the pellentesque veliten.",
        "Đội ngũ hướng dẫn viên bản địa am hiểu địa hình, văn hóa và ẩm thực Hà Tĩnh.",
    ),
    (
        "Hotel ut nisl quam nestibulum ac quam nec odio elementum sceisue the duru ligula. Orci varius natoque penatibus et magnis dis parturient monte nascete ridiculus mus nellentesque habitant morbine.",
        "Liên hệ hotline hoặc form bên cạnh để nhận lịch trình mẫu và báo giá trong ngày làm việc.",
    ),
    (
        "Nulla quis efficitur lacus sulvinar suere ausue in eduis euro vesatien arcuman ontese auctor ac aleuam aretra.",
        "Hơn 10 năm kinh nghiệm dẫn tour tại Hà Tĩnh, am hiểu văn hóa và địa phương.",
    ),
    (
        "Hành trình asue metus the nec feusiate era the miss hendreri the vemante the lemon insan toleon nectan feugiat erat hendrerit necuis vesaire tours inilla neca ine the sene miss habitan.",
        "Tour Thiên Cầm rất tuyệt — hướng dẫn viên nhiệt tình, lịch trình hợp lý cho cả gia đình.",
    ),
    ("Guest review", "Đánh giá khách"),
    (">Phone<", ">Điện thoại<"),
    (">Location<", ">Địa chỉ<"),
    ("Your Number *", "Số điện thoại *"),
    ("Subject *", "Chủ đề *"),
    ("Your message was sent successfully.", "Tin nhắn đã được gửi (demo)."),
    ("1616 Broadway NY, New York 10001", "TP. Hà Tĩnh, Việt Nam"),
    ("United States of America", ""),
    ("5 things you can not miss in Miami", "5 điều không thể bỏ qua ở Thiên Cầm"),
    ("Family Adventure Tour for Teens &amp; Kids", "Tour gia đình khám phá Hà Tĩnh"),
    ("Small group tours with flights from the USA", "Tour nhóm nhỏ khám phá ven biển"),
    ("Most Popular Yacht Charter Routes", "Lộ trình biển được yêu thích"),
    ("Tips Towards a Flawless Honeymoon", "Gợi ý cho chuyến đi tuần trăng mật"),
    (">Travel<", ">Du lịch<"),
    ("Parma", "Can Lộc"),
    ("Aosta", "Hồng Lĩnh"),
    ("Venice", "Cẩm Xuyên"),
    ("Milano", "TP. Hà Tĩnh"),
    ("Normandiya", "Thiên Cầm"),
    ("Bordeaux", "Hương Tích"),
    ("Marseille", "Đồng Lộc"),
    ("Lyon", "Kỳ Anh"),
    ("Cannes", "Cảng cá"),
    ("1 Day Tour", "1 ngày"),
    ("2-4 Days Tour", "2–4 ngày"),
    ("5-7 Days Tour", "5–7 ngày"),
    ("7+ Days Tour", "Trên 7 ngày"),
    ("All Tour", "Xem tất cả tour"),
    (
        "Quisque imperdiet sapien porttito the bibendum sellentesque the commodo erat acar accumsa lobortis, enim diam the nesuen.",
        "Ha Tinh Travel — công ty du lịch địa phương, thiết kế hành trình biển, hồ Kẻ Gỗ và di tích lịch sử tại Hà Tĩnh.",
    ),
    ("Email Địa chỉ", "Email"),
    ("e-Mail Địa chỉ", "Email"),
]

TRAVOL_MAP = (
    'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d97442!2d105.901!3d18.343!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x31384aa2d8f6b743%3A0x7d7f4345e2b2b2b2!2sTh%C3%A0nh%20ph%E1%BB%91%20H%C3%A0%20T%C4%A9nh!5e0!3m2!1svi!2s!4v1'
)


def fix_travol():
    active_map = {
        "index.html": "home",
        "about.html": "about",
        "tours.html": "tours",
        "destination.html": "dest",
        "gallery.html": "gallery",
        "contact.html": "contact",
    }
    repl = TRAVOL_REPL
    folder = ROOT / "travol-duruthemes"
    for page, active in active_map.items():
        fp = folder / page
        if not fp.exists():
            continue
        html = fp.read_text(encoding="utf-8")
        keys = {k: " active" if k == active else "" for k in ("home", "about", "tours", "dest", "gallery", "contact")}
        nav = TRAVOL_NAV.format(**keys)
        html = re.sub(
            r'<div class="collapse navbar-collapse" id="navbar">.*?</div>\s*\n\s*</div>\s*\n\s*</nav>',
            f'<div class="collapse navbar-collapse" id="navbar">\n{nav}\n            </div>\n        </div>\n    </nav>',
            html,
            count=1,
            flags=re.S,
        )
        html = re.sub(r'<a class="logo" href="index\.html">.*?</a>', LOGO, html, count=1, flags=re.S)
        for a, b in repl:
            html = html.replace(a, b)
        html = re.sub(
            r'src="https://www\.google\.com/maps/embed\?pb=[^"]+"',
            f'src="{TRAVOL_MAP}"',
            html,
        )
        html = strip_vendor_links(html)
        html = fix_forms(html)
        if 'lang="vi"' not in html[:400]:
            html = html.replace("<html", '<html lang="vi"', 1)
        fp.write_text(html, encoding="utf-8")
    print("travol fixed")


def remove_nested_div(html: str, marker: str) -> str:
    idx = html.find(marker)
    if idx < 0:
        return html
    start = html.rfind("<div", 0, idx)
    depth = 0
    i = start
    while i < len(html):
        if html.startswith("<div", i):
            depth += 1
            i = html.find(">", i) + 1
        elif html.startswith("</div>", i):
            depth -= 1
            i += 6
            if depth == 0:
                return html[:start] + html[i:]
        else:
            i += 1
    return html


def fix_asatha():
    pages = list((ROOT / "asatha-luxury-webflow").glob("*.html"))
    hide = "<style>.template-popup-wrapper,.showcase-dropdown-wrapper,.showcase-dropdown{display:none!important}</style>"
    text = [
        ("Asatha Luxury - Webflow HTML website template", "Ke Go Retreat — Nghỉ dưỡng cao cấp Hà Tĩnh"),
        ("Asatha", "Ke Go Retreat"),
        ("ASATHA", "KE GO RETREAT"),
        ("Timeless luxury, <em class=\"wood-700-text\">crafted for you</em>", "Nghỉ dưỡng giữa thiên nhiên <em class=\"wood-700-text\">Hà Tĩnh</em>"),
        ("Asatha was created with one vision", "Ke Go Retreat được tạo nên với một tầm nhìn"),
        ("to redefine the art of luxury hospitality", "mang đến trải nghiệm nghỉ dưỡng cao cấp giữa thiên nhiên"),
        ("Dine at Asatha", "Ẩm thực tại Ke Go"),
        ("Dine at Ke Go Retreat", "Ẩm thực tại Ke Go"),
        ("View Details", "Xem chi tiết"),
        ("About Us", "Giới thiệu"),
        ("Contact", "Liên hệ"),
        ("Explore Package", "Xem gói"),
        ("Explore KE GO RETREAT Story", "Câu chuyện Ke Go"),
        ("Check Availability", "Kiểm tra phòng"),
        ("Indian Ocean", "biển Hà Tĩnh"),
        ("Uluwatu", "Thiên Cầm"),
        ("Rooms &amp; Suites", "Phòng & Villa"),
        ("Rooms & Suites", "Phòng & Villa"),
        ("Reserve Stay", "Đặt phòng"),
        ("Email Address", "Email"),
        ("Wellness", "Spa & wellness"),
        ("More Templates", ""),
        ("Style Guide", ""),
        ("Changelog", ""),
        ("Licenses", ""),
        ("Book Your Stay", "Đặt kỳ nghỉ"),
        ("Check Availability", "Khám phá retreat"),
        ("Booking with Airbase", "Đặt phòng demo"),
        ("About us", "Giới thiệu"),
        ("Villas &amp; Suites", "Villa & Suites"),
        ("Packages", "Gói nghỉ dưỡng"),
        ("News &amp; Blogs", "Tin tức"),
        ("Contact Us", "Liên hệ"),
        ("Explore Our Restaurant", "Khám phá nhà hàng"),
        ("Cultural Package", "Gói văn hóa Hà Tĩnh"),
        ("Wellness Escape", "Gói wellness"),
        ("Journey into Bali", "Hành trình khám phá Hà Tĩnh"),
        ("Bali", "Hà Tĩnh"),
        ("Flowcub", ""),
        ("Follow @ASATHA", "Theo dõi @KeGoRetreat"),
        ("$2,999", "3.500.000đ"),
        ("$1,125", "2.200.000đ"),
        ("Where time slows, Comfort deepens", "Chậm lại giữa thiên nhiên Hà Tĩnh"),
        ("Private spaces, thoughtful service, and the quiet luxury of feeling at home.", "Không gian riêng tư, dịch vụ chu đáo và cảm giác an yên."),
        ("Guest stories", "Cảm nhận khách hàng"),
        ("About our villas and resort", "Villa và resort Ke Go"),
        ("Discover spaces designed for unhurried living.", "Không gian thiết kế cho nhịp sống thong dong."),
        ("An Award-winning escape", "Kỳ nghỉ đáng nhớ"),
        ("Made by design.", ""),
        ("Powered by .", ""),
        ("Jl. Labuan Sait", "Khu vực Thiên Cầm"),
        ("Pecatu, South Kuta, Badung Regency", "Thiên Cầm, Hà Tĩnh"),
        ("Choose Services*", "Dịch vụ*"),
        ("Choose Villa & Suites*", "Loại phòng*"),
        ("Select room*", "Chọn phòng*"),
        ("Check-in*", "Nhận phòng*"),
        ("Check-out*", "Trả phòng*"),
        ("Adults (Age 21+)*", "Người lớn*"),
        ("Children (Ages 2–12)*", "Trẻ em*"),
        ("Ke Go Retreat Rewards", "Ưu đãi Ke Go Retreat"),
        ("Popular Gói nghỉ dưỡng", "Gói nghỉ dưỡng phổ biến"),
        ("Đặt kỳ nghỉ của bạn", "Đặt kỳ nghỉ"),
        ("Every corner of Ke Go Retreat felt intentional", "Mỗi góc Ke Go Retreat đều được chăm chút"),
        ("Rooted in warmth and inspired by nature", "Gắn với thiên nhiên và sự ấm áp"),
        ("Set on dramatic cliffs overlooking", "Tọa lạc giữa cảnh quan"),
        ("boutique living and the serenity of nature", "không gian boutique và sự tĩnh lặng"),
        ("200+ happy guests so far", "Hơn 200 khách hài lòng"),
        ("Wake up to endless ocean horizons", "Thức dậy cùng biển trời Hà Tĩnh"),
        ("Check <em class=\"wood-700-text\">Availability</em>", "Kiểm tra <em class=\"wood-700-text\">phòng trống</em>"),
        ("You'll receive a confirmation within 24h.", "Chúng tôi phản hồi trong vòng 24 giờ."),
        ("You’ll receive a confirmation within 24h.", "Chúng tôi phản hồi trong vòng 24 giờ."),
        ("Select one...", "Chọn..."),
        ("Boutique villas, bespoke experiences, and timeless comfort - crafted for those who seek more than just a stay.", "Villa boutique, trải nghiệm riêng và sự thoải mái — dành cho ai muốn hơn cả một kỳ nghỉ."),
        ("4.9 | 15k+ Reviews", "4.9 | 15k+ đánh giá"),
        ("Follow @KE GO RETREAT", "Theo dõi @KeGoRetreat"),
        (">MENU<", ">Menu<"),
        ("MENU", "Menu"),
        ("Homepage", "Trang chủ"),
        ("Quick Links", "Liên kết nhanh"),
        ("Guest <em class=\"wood-700-text\">stories</em>", "Cảm nhận <em class=\"wood-700-text\">khách hàng</em>"),
        ("Infinity Pool", "Hồ bơi vô cực"),
        ("Oceanfront Yoga", "Yoga ven biển"),
        ("Spa & wellness &amp; Spa Space", "Không gian spa & wellness"),
        ("Children's play area", "Khu vui chơi trẻ em"),
        ("Villas And Suites", "Villa & Suites"),
        ("An intimate journey of flavors, crafted with care and served against a backdrop of timeless beauty.", "Hành trình ẩm thực tinh tế, phục vụ trong không gian đẹp và yên bình."),
        (", we offer not just a destination, but a sanctuary where every moment is designed to be unforgettable.", " — nơi mỗi khoảnh khắc đều đáng nhớ."),
        ("we offer not just a destination, but a sanctuary where every moment is designed to be unforgettable.", "mang đến không gian an yên, mỗi khoảnh khắc đều đáng nhớ."),
        ("Ke Go Retreat is a luxury  template for resorts", "Ke Go Retreat — nghỉ dưỡng cao cấp tại Hà Tĩnh"),
        (", private villas, and wellness retreats. Crafted to highlight suites, spa experiences, dining, and curated packages — with elegant design that inspires direct bookings.", " — villa, spa, ẩm thực và gói nghỉ dưỡng giữa thiên nhiên Hà Tĩnh."),
        ("Powered by", ""),
        (" design.", ""),
        ("Discover spaces", "Khám phá không gian"),
        ("Ke Go Retreat is where <em>you feel restored.</em>", "Ke Go Retreat — nơi bạn <em>tìm lại sự an yên.</em>"),
        (
            "A haven where thoughtful design and unspoiled surroundings create an experience of quiet luxury.",
            "Nơi thiết kế tinh tế và thiên nhiên nguyên sơ tạo nên trải nghiệm nghỉ dưỡng thanh bình.",
        ),
        ("Feature spa, yoga, and wellness retreats with calming visuals and retreat menus. Ideal  layout for resorts offering premium wellness experiences.", "Spa, yoga và gói wellness giữa thiên nhiên Hà Tĩnh."),
        ("Showcase luxury villas, suites, and private stays. A  template page for resorts offering curated accommodations with filters and guest reviews.", "Villa và suite cao cấp giữa thiên nhiên Hà Tĩnh."),
        ("Sunset Estate", "Villa Hoàng Hôn"),
        ("Skyline Villa", "Villa Tầng Mây"),
        ("Garden Villa", "Villa Vườn Xanh"),
        ("Oceanfront Pavilion", "Pavilion Ven Biển"),
        ("Clifftop Mansion", "Mansion Đỉnh Đồi"),
        ("Cliffside Villa", "Villa Vách Đá"),
        ("Serenity Suite", "Suite An Yên"),
        ("Amber Suite", "Suite Amber"),
        ("The Pavilion Residence", "Residence Pavilion"),
        ("Love Package", "Gói đôi"),
        ("Family Retreat", "Gói gia đình"),
        ("Cultural Package", "Gói văn hóa"),
        ("Wellness Escape", "Gói wellness"),
        ("Discover More", "Xem thêm"),
        ("Discover Khác", "Xem thêm"),
        ("Read More", "Đọc thêm"),
        ("Read Khác", "Đọc thêm"),
        ("More", "Khác"),
        (
            "Discover a perfect balance of refined luxury and natural harmony.",
            "Khám phá sự cân bằng giữa sang trọng và thiên nhiên.",
        ),
        (
            "Discover sound therapy, breathwork, and energy-balancing rituals designed to calm the mind and renew the body.",
            "Trị liệu âm thanh, thở và nghi thức cân bằng năng lượng — thư giãn tâm trí và tái tạo cơ thể.",
        ),
        (
            "Discover a selection of our finest culinary offerings",
            "Khám phá các món tinh hoa trong thực đơn",
        ),
        ("Aqua ocean <em class=\"wood-700-text\">explorer cruise</em>", "Du thuyền <em class=\"wood-700-text\">khám phá biển</em>"),
        ("@Yachts &amp; jets", "@Du thuyền &amp; tour biển"),
        ("Submit", "Gửi"),
        ("Send Message", "Gửi tin nhắn"),
        ("Your Name", "Họ và tên"),
        ("Message", "Nội dung"),
    ]
    core = {"index.html", "about-us.html", "villas-and-suites.html", "wellness.html", "dining.html", "contact-us.html"}
    folder = ROOT / "asatha-luxury-webflow"
    for fp in pages:
        html = fp.read_text(encoding="utf-8")
        if hide not in html:
            html = html.replace("</head>", hide + "</head>", 1)
        html = remove_nested_div(html, 'class="template-popup-wrapper"')
        for a, b in text:
            html = html.replace(a, b)
        html = re.sub(
            r"Discover a perfect balance of refined luxury and natural wonder[^<]{0,120}",
            "Khám phá sự cân bằng giữa sang trọng và thiên nhiên tại Ke Go Retreat.",
            html,
        )
        html = re.sub(
            r"Discover sound therapy, breathwork, and energy-balancing sessions[^<]{0,120}",
            "Trị liệu âm thanh, thở và cân bằng năng lượng — thư giãn tâm trí và tái tạo cơ thể.",
            html,
        )
        if fp.name in core:
            imgs = [
                "18_hero_ke_go_lake_misty_morning.png",
                "19_hospitality_forest_lake_lodge.png",
                "20_hospitality_villa_infinity_pool_sunset.png",
                "58_hospitality_beach_villa_twilight_pool.png",
                "38_hospitality_quiet_lake_resort.png",
                "28_hospitality_resort_pool_evening.png",
                "57_hospitality_lake_resort_village.png",
                "26_hospitality_beach_restaurant_sunset.png",
                "59_hospitality_seaside_dining_balcony.png",
                "30_hospitality_lake_lodge_hatinh.png",
            ]
            idx = 0

            def img_repl(m):
                nonlocal idx
                if idx >= len(imgs):
                    return m.group(0)
                if "logo" in m.group(1).lower() or ".svg" in m.group(1):
                    return m.group(0)
                path = p(imgs[idx])
                idx += 1
                return f'src="{path}"'

            html = re.sub(
                r'src="(assets/cdn\.prod\.website-files\.com/[^"]+\.(?:webp|jpg|jpeg|png))"',
                img_repl,
                html,
            )
        html = strip_vendor_links(html)
        html = fix_forms(html)
        html = html.replace('lang="en"', 'lang="vi"')
        fp.write_text(html, encoding="utf-8")
    print("asatha fixed")


def fix_colorlib():
    pages = ["index.html", "about.html", "rooms.html", "restaurant.html", "contact.html"]
    folder = ROOT / "colorlib-deluxe"
    text = [
        ("Deluxe Khách sạn Ha Tinh - Free Bootstrap 4 Template by ", "Deluxe Hotel Ha Tinh — Lưu trú tiện nghi"),
        ("Deluxe Khách sạn Ha Tinh", "Deluxe Hotel Ha Tinh"),
        ("Chào mừng To Deluxe Khách sạn Ha Tinh", "Lựa chọn lưu trú tiện nghi tại Hà Tĩnh"),
        ("Chào mừng To Deluxe Hotel Ha Tinh", "Lựa chọn lưu trú tiện nghi tại Hà Tĩnh"),
        ("Khách sạns &amp; Resorts", "Khách sạn tại Hà Tĩnh"),
        ("Khách sạn &amp; Resorts", "Khách sạn tại Hà Tĩnh"),
        ("index-1.html", "index.html"),
        (">Home<", ">Trang chủ<"),
        (">Restaurant<", ">Ẩm thực<"),
        (">About<", ">Giới thiệu<"),
        (">Blog<", ">Tin tức<"),
        (">Rooms<", ">Phòng<"),
        ("Book Now", "Xem phòng"),
        ("Check Availability", "Kiểm tra phòng"),
        ("Free Bootstrap 4 Template by ", ""),
        ("Colorlib", ""),
        ("Liên hệ Us", "Liên hệ"),
    ]
    bg_map = [
        ("images/bg_1.jpg", p("08_hospitality_hospitality_beachfront_resort.png")),
        ("images/bg_2.jpg", p("17_hospitality_modern_beach_hotel_exterior.png")),
        ("images/room-1.jpg", p("09_hospitality_hospitality_sea_view_room.png")),
        ("images/room-2.jpg", p("29_hospitality_luxury_sea_view_room.png")),
        ("images/room-3.jpg", p("60_hospitality_sea_view_room_bright.png")),
        ("images/room-4.jpg", p("45_hospitality_luxury_seaside_hotel_room.png")),
        ("images/food-1.jpg", p("26_hospitality_beach_restaurant_sunset.png")),
        ("images/food-2.jpg", p("40_hospitality_seaside_restaurant_sunset.png")),
        ("images/about.jpg", p("17_hospitality_modern_beach_hotel_exterior.png")),
    ]
    for i in range(1, 9):
        bg_map.append(
            (f"images/menu-{i}.jpg", p("26_hospitality_beach_restaurant_sunset.png" if i % 2 else "40_hospitality_seaside_restaurant_sunset.png"))
        )
    for page in pages:
        fp = folder / page
        if not fp.exists():
            continue
        html = fp.read_text(encoding="utf-8")
        for a, b in text:
            html = html.replace(a, b)
        for a, b in bg_map:
            html = html.replace(a, b)
        html = strip_vendor_links(html)
        html = fix_forms(html)
        fp.write_text(html, encoding="utf-8")
    print("colorlib fixed")


HOTALE_NAV = """<ul id="menu-main-navigation-1" class="sf-menu">
                                        <li class="menu-item menu-item-home{home_cls} hotale-normal-menu"><a href="index.html">Trang chủ</a></li>
                                        <li class="menu-item{about_cls} hotale-normal-menu"><a href="about-us.html">Giới thiệu</a></li>
                                        <li class="menu-item{rooms_cls} hotale-normal-menu"><a href="room-grid-style-1.html">Phòng</a></li>
                                        <li class="menu-item{dining_cls} hotale-normal-menu"><a href="price-table.html">Ẩm thực</a></li>
                                        <li class="menu-item{gallery_cls} hotale-normal-menu"><a href="gallery.html">Gallery</a></li>
                                        <li class="menu-item{contact_cls} hotale-normal-menu"><a href="contact.html">Liên hệ</a></li>
                                    </ul>"""

HOTALE_MOBILE = """<div class="mm-panels"><div class="mm-panel mm-hasnavbar mm-opened mm-current" id="menu-main-navigation"><div class="mm-navbar"><a class="mm-title"><span class="mmenu-custom-close"></span></a></div><ul class="m-menu mm-listview">
                                <li class="menu-item menu-item-home{home_cls}"><a href="index.html">Trang chủ</a></li>
                                <li class="menu-item{about_cls}"><a href="about-us.html">Giới thiệu</a></li>
                                <li class="menu-item{rooms_cls}"><a href="room-grid-style-1.html">Phòng</a></li>
                                <li class="menu-item{dining_cls}"><a href="price-table.html">Ẩm thực</a></li>
                                <li class="menu-item{gallery_cls}"><a href="gallery.html">Gallery</a></li>
                                <li class="menu-item{contact_cls}"><a href="contact.html">Liên hệ</a></li>
                            </ul></div></div></div>"""

HOTALE_MAP = (
    'src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3812!2d106.058!3d18.047'
    "!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zVGjGnDoSBp4biBIw6AgVMmFt"
    '!5e0!3m2!1svi!2s!4v1"'
)


def fix_hotale_core():
    active_map = {
        "index.html": "home",
        "about-us.html": "about",
        "room-grid-style-1.html": "rooms",
        "price-table.html": "dining",
        "gallery.html": "gallery",
        "contact.html": "contact",
    }
    blog_fix = [
        ("Cities To Visit For Your First Time In Europe", "Khám phá Thiên Cầm mùa hè"),
        ("Where to travel in 2022: 10 places you need to go in 2022!", "5 điểm đến nên ghé tại Hà Tĩnh"),
        ("Tips For Picking Vacation Accommodation", "Gợi ý chọn phòng nghỉ dưỡng"),
        ("What to expect on an African Safari?", "Trải nghiệm biển và ẩm thực địa phương"),
        ("My 6 Biggest Travel Surprises", "Những điều du khách thích ở Thiên Cầm"),
        ("10 Tips for Taking Your First Solo Trip", "10 mẹo du lịch Hà Tĩnh tự túc"),
        ("Why I Quit My Job To Be A Less Occasional Traveller In 2019", "Kỳ nghỉ ngắn ngày tại Thiên Cầm"),
        ("Where To Travel In Asia From January To June", "Lịch trình gợi ý theo mùa"),
        ("3 steps to discovering your life's purpose", "Gợi ý lịch trình nghỉ dưỡng"),
        ("News & Offers", "Tin tức & ưu đãi"),
        ("Read the blog", "Xem tin tức"),
        ("Newsletter", "Nhận tin"),
        ("Your Email Address", "Email của bạn"),
        ("Subscribe", "Đăng ký"),
        ("Room Grid Style 1", "Danh sách phòng"),
        ("Room Grid Style 2", "Phòng kiểu 2"),
        ("Room Grid Style 3", "Phòng kiểu 3"),
        ("Room Grid Style 4", "Phòng kiểu 4"),
        ("Room Modern Style", "Phòng hiện đại"),
        ("Room Side Thumbnail", "Phòng thumbnail"),
        (">Home<", ">Trang chủ<"),
        (">Home –", ">Trang chủ –"),
        (">Pages<", ">Trang<"),
        (">Blog<", ">Tin tức<"),
        ("Reservation", "Đặt phòng"),
        ("Price Table", "Ẩm thực"),
        ("Our Team", "Đội ngũ"),
        ("Resort Review", "Đánh giá resort"),
        (">About<", ">Giới thiệu<"),
        ("3 Michelin Stars Ẩm thực, Vézère", "Ẩm thực biển địa phương"),
        ("test@gmail.com", "contact@thiencam.demo"),
        ("1-634-567-34", "0239 385 6789"),
        ("Madrid", "Hà Tĩnh"),
        ("Del Ejercito", "Thiên Cầm"),
        ("Kingston UK", "Hà Tĩnh"),
        ("Peterson Street", "Thiên Cầm"),
        ("Login", "Đăng nhập"),
        ("Sign Up", "Đăng ký"),
        ("Forgot Password?", "Quên mật khẩu?"),
        (">Register<", ">Đăng ký<"),
        ("3 steps to discovering your life's purpose", "Gợi ý lịch trình nghỉ dưỡng"),
        ("3 steps to discovering your life's purpose", "Gợi ý lịch trình nghỉ dưỡng"),
        ("Del Ejercito", "Thiên Cầm"),
        ("Av. del Ejercito", "Thiên Cầm"),
        ("News & Offers", "Tin tức & ưu đãi"),
        ("Forget Password?", "Quên mật khẩu?"),
        ("Username or E-Mail", "Email"),
        ("Do not have an account?", "Chưa có tài khoản?"),
        ("Privacy Policy", "Chính sách"),
        ("Hotale – Hotel HTML Template", "Thien Cam Resort — Resort ven biển Hà Tĩnh"),
        ("Book Now", "Đặt phòng"),
        ("data-label=\"Book Now\"", "data-label=\"Đặt phòng\""),
        ("Hotale Av.", "Thiên Cầm"),
        ("Thien Cam Resort Av.", "Thiên Cầm"),
        ("Kỳ nghỉ ven biển tại Thiên Cầm", "Kỳ nghỉ ven biển trọn vẹn tại Thiên Cầm"),
        ("Theme's Elements", "Thực đơn resort"),
        ("Example of price table", "Gợi ý thực đơn"),
        ("Ẩm thực With Featured", "Thực đơn nổi bật"),
        ("Starter Plan", "Gói cơ bản"),
        ("Suitable for starter", "Phù hợp khởi đầu"),
        ("Hotel Review", "Đánh giá resort"),
        (">Contact<", ">Liên hệ<"),
        (">Rooms<", ">Phòng<"),
        (">FAQ<", ">Hỏi đáp<"),
        ("About Us 2", "Giới thiệu 2"),
        ("About Us 3", "Giới thiệu 3"),
        ("Coming Soon", "Sắp ra mắt"),
        ("Maintenance", "Bảo trì"),
        ("3 steps to discovering your life's purpose", "Gợi ý lịch trình nghỉ dưỡng"),
        ("News &amp; Offers", "Tin tức &amp; ưu đãi"),
        ("Safe", "Két an toàn"),
        ("Gym", "Phòng gym"),
        (", a fresh and modern place to visit and enjoy dishes always handmade of the best ingredients of the season.", " — không gian hiện đại, món ăn tươi theo mùa."),
        (", An iconic american bar", " — bar cocktail ven biển"),
        (" or a pampering moment on the massage table and inside the warm saunas, you can always find a place for yourself at our spa.", " — massage, xông hơi và không gian thư giãn riêng tư."),
        ("del Ejercito, 2, 1900", "Khu vực Thiên Cầm"),
    ]
    hotale_vi = [
        ("Deluxe Suite Room", "Phòng Deluxe"),
        ("Luxury Suite", "Suite hạng sang"),
        ("Standard Deluxe", "Deluxe tiêu chuẩn"),
        ("The Penthouse", "Penthouse view biển"),
        ("Grand Suite Room", "Suite lớn"),
        ("Junior Suite Room", "Suite junior"),
        ("Standard Room", "Phòng tiêu chuẩn"),
        ("Family Special Room", "Phòng gia đình"),
        ("Premium Room", "Phòng cao cấp"),
        (">From<", ">Từ<"),
        ("/ night", "/ đêm"),
        ("4 Guests", "4 khách"),
        ("6 Guests", "6 khách"),
        ("3 Guests", "3 khách"),
        ("1 King Bed", "1 giường king"),
        ("2 King Beds", "2 giường king"),
        ("2 Single Beds", "2 giường đơn"),
        ("1 Double Bed", "1 giường đôi"),
        ("2 Double Beds", "2 giường đôi"),
        ("20% Off", "Giảm 20%"),
        ("15% Off", "Giảm 15%"),
        ("30% Off", "Giảm 30%"),
        ("$250", "6.200.000đ"),
        ("$200", "5.000.000đ"),
        ("$180", "4.500.000đ"),
        ("$150", "3.800.000đ"),
        ("$105", "2.600.000đ"),
        ("$90", "2.200.000đ"),
        ("$80", "1.950.000đ"),
        ("$75", "1.850.000đ"),
        ("$69", "1.700.000đ"),
        ("Parking", "Bãi đỗ xe"),
        ("Swimming Pool", "Hồ bơi"),
        ("Free Wifi", "Wifi miễn phí"),
        ("Breakfast", "Bữa sáng"),
        ("Workspace", "Không gian làm việc"),
        ("Testimonial", "Đánh giá khách"),
        ("Visit Our Famous Tiện ích", "Khám phá tiện ích resort"),
        ("Visit Our Famous", "Khám phá"),
        ("The Penthouse Bar, An iconic american bar", "Bar Penthouse — cocktail ven biển"),
        ("The Spa. Refresh Yourself", "Spa — thư giãn toàn thân"),
        ("A brasserie inspired by French cuisine", "Nhà hàng hải sản và đặc sản địa phương"),
        ("The cozy bar area accompanying the Penthouse", "Không gian bar ấm cúng nhìn ra biển"),
        ("classic cocktail bar", "bar cocktail"),
        ("bewerages", "đồ uống"),
        ("Whether you are in search of a well-appointed gym", "Phòng gym và spa hiện đại"),
        ("Follow us on Instagram", "Theo dõi trên Instagram"),
        ("5 stars 25 rooms", "5 sao · 25 phòng"),
        ("Solo Traveler", "Khách lẻ"),
        ("Solo Traveller", "Khách lẻ"),
        ("Joan Smith", "Nguyễn Thu Hà"),
        ("William Jones", "Trần Minh Anh"),
        ("Ralph Clark", "Lê Văn Đức"),
        ("Christopher Lopez", "Phạm Hoàng Nam"),
        ("Louis Lewis", "Hoàng Thị Lan"),
        ("Guests", "Khách"),
        ("Check In", "Nhận phòng"),
        ("Check Out", "Trả phòng"),
        ("Adult", "Người lớn"),
        ("Children", "Trẻ em"),
    ]
    room_imgs = [
        "09_hospitality_hospitality_sea_view_room.png",
        "29_hospitality_luxury_sea_view_room.png",
        "45_hospitality_luxury_seaside_hotel_room.png",
        "60_hospitality_sea_view_room_bright.png",
        "35_hospitality_peaceful_beach_resort.png",
        "48_hospitality_beach_resort_golden_hour.png",
        "08_hospitality_hospitality_beachfront_resort.png",
        "17_hospitality_modern_beach_hotel_exterior.png",
    ]
    folder = ROOT / "hotale-resort"
    for page, active in active_map.items():
        fp = folder / page
        if not fp.exists():
            continue
        html = fp.read_text(encoding="utf-8")
        cls = lambda k: " current-menu-item" if k == active else ""
        nav = HOTALE_NAV.format(
            home_cls=cls("home"),
            about_cls=cls("about"),
            rooms_cls=cls("rooms"),
            dining_cls=cls("dining"),
            gallery_cls=cls("gallery"),
            contact_cls=cls("contact"),
        )
        html = re.sub(
            r'<ul id="menu-main-navigation-1" class="sf-menu">.*?<div class="hotale-navigation-slide-bar',
            nav + '\n                                    <div class="hotale-navigation-slide-bar',
            html,
            count=1,
            flags=re.S,
        )
        mobile = HOTALE_MOBILE.format(
            home_cls=cls("home"),
            about_cls=cls("about"),
            rooms_cls=cls("rooms"),
            dining_cls=cls("dining"),
            gallery_cls=cls("gallery"),
            contact_cls=cls("contact"),
        )
        html = re.sub(
            r'<div class="mm-panels">.*?</div></div>\s*<div class="hotale-mobile-header-wrap">',
            mobile + '\n\n    <div class="hotale-mobile-header-wrap">',
            html,
            count=1,
            flags=re.S,
        )
        html = re.sub(
            r'src="https://www\.google\.com/maps/embed\?[^"]+"',
            HOTALE_MAP,
            html,
        )
        for a, b in blog_fix + hotale_vi:
            html = html.replace(a, b)
        html = re.sub(
            r"A wonderful serenity has taken possession[^<]{0,400}",
            "Không gian resort thoải mái, gần biển Thiên Cầm — phù hợp kỳ nghỉ gia đình.",
            html,
        )
        html = re.sub(
            r"Không gian resort thoải mái, gần biển Thiên Cầm — phù hợp kỳ nghỉ gia đình\.[^<]{0,300}",
            "Không gian resort thoải mái, gần biển Thiên Cầm — phù hợp kỳ nghỉ gia đình.",
            html,
        )
        html = re.sub(
            r"3 steps to discovering your life.s purpose",
            "Gợi ý lịch trình nghỉ dưỡng",
            html,
        )
        html = re.sub(r"\b5 stars 25 rooms\b", "5 sao · 25 phòng", html)
        html = re.sub(
            r"Không gian bar ấm cúng nhìn ra biển is a bar cocktail[^<]{0,200}",
            "Không gian bar ấm cúng nhìn ra biển — cocktail và đồ uống đặc sắc.",
            html,
        )
        idx = 0

        def hotale_img(m):
            nonlocal idx
            src = m.group(1)
            if "logo" in src or "footer" in src or "banner" in src or "card" in src:
                return m.group(0)
            if idx >= len(room_imgs):
                return m.group(0)
            path = p(room_imgs[idx])
            idx += 1
            return f'src="{path}"'

        html = re.sub(
            r'src="(assets/max-themes\.net/demos/hotale/hotale/resort/upload/[^"]+\.(?:jpg|jpeg|png))"',
            hotale_img,
            html,
        )
        html = strip_vendor_links(html)
        html = fix_forms(html)
        fp.write_text(html, encoding="utf-8")
    print("hotale core fixed")


def fix_moonlit():
    pages = ["index.html", "about.html", "room-one.html", "gallery.html", "contact.html"]
    folder = ROOT / "moonlit-react"
    text = [
        ("Moonlit - Hotel and Resturant React Js Template", "Moonlit Hotel Ha Tinh — Khách sạn hiện đại"),
        ("Moonlit - Hotel and Resort React Js Template", "Moonlit Hotel Ha Tinh — Khách sạn hiện đại"),
        ("Moonlit Hotel Ha Tinh Hotel", "Moonlit Hotel Ha Tinh"),
        ("Moonlit Hotel Ha Tinh Ha Tinh", "Moonlit Hotel Ha Tinh"),
        ("Moonlit Hotel Ha Tinh - Khách sạn Hà Tĩnh React Js Template", "Khách sạn hiện đại cho chuyến đi Hà Tĩnh"),
        ("React Js Template", ""),
        ("Book Now", "Xem phòng"),
        ("Check In", "Nhận phòng"),
        ("Check Out", "Trả phòng"),
        ("About Us", "Giới thiệu"),
        ("Our Rooms", "Phòng nghỉ"),
        ("Contact Us", "Liên hệ"),
        ("Restaurant", "Nhà hàng"),
        ("Discover", "Khám phá"),
        ("Luxury Hotel", "Khách sạn Hà Tĩnh"),
    ]
    imgs = ["08_hospitality_hospitality_beachfront_resort.png", "17_hospitality_modern_beach_hotel_exterior.png",
            "09_hospitality_hospitality_sea_view_room.png", "29_hospitality_luxury_sea_view_room.png",
            "45_hospitality_luxury_seaside_hotel_room.png", "48_hospitality_beach_resort_golden_hour.png"]
    for page in pages:
        fp = folder / page
        if not fp.exists():
            continue
        html = fp.read_text(encoding="utf-8")
        for a, b in text:
            html = html.replace(a, b)
        idx = 0
        def img_repl(m):
            nonlocal idx
            src = m.group(1)
            if "logo" in src.lower() or ".svg" in src.lower() or "shape" in src.lower() or "icon" in src.lower():
                return m.group(0)
            if idx >= len(imgs):
                return m.group(0)
            path = p(imgs[idx])
            idx += 1
            return f'src="{path}"'
        html = re.sub(r'src="(assets/moonlit-react\.netlify\.app/assets/images/[^"]+\.(?:jpg|jpeg|png|webp))"', img_repl, html)
        html = fix_forms(html)
        html = html.replace('lang="en"', 'lang="vi"')
        fp.write_text(html, encoding="utf-8")
    print("moonlit fixed")


def fix_framer(slug: str, brand: str, hero_hint: str, imgs: list[str]):
    folder = ROOT / slug
    pages = sorted(folder.glob("*.html"))
    slug_text = {
        "mountain-lodge-framer": [
            ("Your idyllic weekend retreat", "Chạm vào nhịp sống xanh bên hồ Kẻ Gỗ"),
            ("Tranquil Escape", "Nghỉ dưỡng an yên"),
            ("BOOK YOUR STAY", "ĐẶT PHÒNG"),
            ("Arcosa, Italy", "Kẻ Gỗ, Hà Tĩnh"),
        ],
        "luxestay-framer": [
            ("The timeless luxury of island living", "Không gian nghỉ dưỡng riêng tư tại Hà Tĩnh"),
            ("Book a stay", "Xem villa"),
            ("Stay.  Explore.  Feel alive", "Ở lại. Khám phá. Tận hưởng Hà Tĩnh"),
        ],
    }.get(slug, [])
    for fp in pages:
        html = fp.read_text(encoding="utf-8")
        html = html.replace("Mountain Eco Lodge", brand)
        html = html.replace("Mountain Lodge", brand)
        html = html.replace("Ke Go Eco Eco Lodge", "Ke Go Eco Lodge")
        html = html.replace("Wanderway", brand).replace("LuxeStay", brand).replace("Luxestay", brand)
        html = html.replace("Book Now", "Đặt phòng").replace("Book now", "Đặt phòng")
        html = html.replace("Contact Us", "Liên hệ").replace("About Us", "Giới thiệu")
        html = html.replace("About us", "Giới thiệu")
        html = html.replace(">Tours<", ">Tour<")
        html = html.replace(">Home<", ">Trang chủ<")
        html = html.replace("Book a Trip Now", "Đặt tour ngay")
        html = html.replace("Start Your Journey", "Bắt đầu hành trình")
        html = html.replace("More About US", "Giới thiệu thêm")
        html = html.replace("More About Us", "Giới thiệu thêm")
        html = html.replace("More about us", "Giới thiệu thêm")
        html = html.replace("European dining", "ẩm thực địa phương")
        html = html.replace("contemporary European", "đặc sản Hà Tĩnh")
        html = html.replace(", Europe", ", Hà Tĩnh")
        html = html.replace("Europe,", "Hà Tĩnh,")
        html = html.replace(">Europe<", ">Hà Tĩnh<")
        html = html.replace(">ABOUT<", ">GIỚI THIỆU<")
        html = html.replace(">About<", ">Giới thiệu<")
        for old, new in slug_text:
            html = html.replace(old, new)
        html = re.sub(r"<a[^>]*>.*?BUY THIS TEMPLATE.*?</a>", "", html, flags=re.I | re.S)
        if "</head>" in html and "framer-buy-badge" not in html:
            html = html.replace(
                "</head>",
                '<style>a[href*="framer.com"],[data-framer-name="Buy"],.framer-1v1xq0x{display:none!important}</style></head>',
                1,
            )
        html = html.replace('lang="en"', 'lang="vi"')
        idx = 0

        def next_path() -> str:
            nonlocal idx
            path = p(imgs[idx % len(imgs)])
            idx += 1
            return path

        def img_repl(_m: re.Match) -> str:
            return f'src="{next_path()}"'

        def url_repl(_m: re.Match) -> str:
            return f"url('{next_path()}')"

        pat = r"(?:https://|assets/)?framerusercontent\.com/images/[^\"')&]+\.(?:jpg|jpeg|png|webp)[^\"')&]*"
        html = re.sub(rf'src="({pat})"', img_repl, html, flags=re.I)
        html = re.sub(rf"url\((['\"]?)({pat})\1\)", url_repl, html, flags=re.I)
        html = re.sub(rf"url\(&quot;({pat})&quot;\)", lambda _m: f"url(&quot;{next_path()}&quot;)", html, flags=re.I)
        html = fix_forms(html)
        fp.write_text(html, encoding="utf-8")
    print(f"{slug} fixed")


def main():
    fix_travol()
    fix_asatha()
    fix_colorlib()
    fix_hotale_core()
    fix_moonlit()
    fix_framer("mountain-lodge-framer", "Ke Go Eco Lodge", "eco", [
        "18_hero_ke_go_lake_misty_morning.png", "56_hero_misty_forest_lake_boat.png",
        "19_hospitality_forest_lake_lodge.png", "30_hospitality_lake_lodge_hatinh.png", "57_hospitality_lake_resort_village.png",
    ])
    fix_framer("wanderway-framer", "Wander Hà Tĩnh", "travel", [
        "01_hero_hero_thien_cam_beach_sunrise.png", "11_hero_wide_beach_sunrise_boats.png",
        "12_destination_coastal_road_mountain_sea.png", "54_lifestyle_friends_beach_walk_sunset.png", "10_experience_experience_ke_go_boat_tour.png",
    ])
    fix_framer("luxestay-framer", "LuxeStay Ha Tinh", "luxury", [
        "15_hospitality_luxury_resort_pool_sunset.png", "20_hospitality_villa_infinity_pool_sunset.png",
        "58_hospitality_beach_villa_twilight_pool.png", "38_hospitality_quiet_lake_resort.png",
    ])


if __name__ == "__main__":
    main()
    import sys

    sys.path.insert(0, str(Path(__file__).parent))
    import fix_showcase

    fix_showcase.main()
