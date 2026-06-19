#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Port Travello template → Hà Tĩnh Discovery demo."""

import os
import re

DEMO_DIR = os.path.dirname(os.path.abspath(__file__))
SHARED = "../assets/shared-images"
ASSET_BASE = "assets/preview.colorlib.com/theme/travello/images/"

# Images stored as scraped full-path src attributes
IMG_SRC_MAP = {
    "destination_1.jpg":  "04_destination_destination_ke_go_lake.png",
    "destination_2.jpg":  "05_destination_destination_huong_tich_pagoda.png",
    "destination_3.jpg":  "24_destination_huong_tich_pagoda_landscape.png",
    "destination_4.jpg":  "25_destination_dong_loc_memorial_aerial.png",
    "destination_5.jpg":  "42_destination_memorial_sunset_quiet.png",
    "destination_6.jpg":  "31_destination_coastal_road_overlook.png",
    "destination_7.jpg":  "13_destination_fishing_boats_sunset_bay.png",
    "destination_8.jpg":  "33_destination_fishing_harbor_sunset.png",
    "destination_9.jpg":  "52_destination_winding_coastal_road_blue_sea.png",
    "why_1.jpg":          "21_experience_kayak_lake_mountain_forest.png",
    "why_2.jpg":          "22_experience_seafood_table_beach.png",
    "why_3.jpg":          "23_culture_traditional_market_hatinh.png",
    "news_1.jpg":         "13_destination_fishing_boats_sunset_bay.png",
    "news_2.jpg":         "33_destination_fishing_harbor_sunset.png",
    "news_3.jpg":         "52_destination_winding_coastal_road_blue_sea.png",
    "latest_1.jpg":       "13_destination_fishing_boats_sunset_bay.png",
    "latest_2.jpg":       "33_destination_fishing_harbor_sunset.png",
    "latest_3.jpg":       "52_destination_winding_coastal_road_blue_sea.png",
    "news_4.jpg":         "23_culture_traditional_market_hatinh.png",
    "news_5.jpg":         "50_culture_fresh_local_market.png",
    "news_6.jpg":         "49_destination_temple_morning_mountains.png",
    "team_1.jpg":         "14_lifestyle_group_travelers_beach_sunset.png",
    "team_2.jpg":         "27_lifestyle_couple_beach_walk_sunset.png",
    "team_3.jpg":         "54_lifestyle_friends_beach_walk_sunset.png",
    "team_4.jpg":         "50_culture_fresh_local_market.png",
    "about_1.jpg":        "14_lifestyle_group_travelers_beach_sunset.png",
}

# Background images referenced as url(images/...)
BG_MAP = {
    "about.jpg":       "01_hero_hero_thien_cam_beach_sunrise.png",
    "destinations.jpg":"32_hero_calm_beach_golden_hour.png",
    "contact.jpg":     "43_hero_empty_beach_morning.png",
    "news.jpg":        "43_hero_empty_beach_morning.png",
    "testimonials.jpg":"11_hero_wide_beach_sunrise_boats.png",
    "travello.jpg":    "18_hero_ke_go_lake_misty_morning.png",
    "footer_1.jpg":    "32_hero_calm_beach_golden_hour.png",
    "why.jpg":         "56_hero_misty_forest_lake_boat.png",
}

# Hero slider 3 slides (all use same original file, differentiate here)
HERO_SLIDES = [
    "03_hero_hero_ke_go_lake_morning.png",
    "01_hero_hero_thien_cam_beach_sunrise.png",
    "41_hero_quiet_lake_sunrise.png",
]

PAGE_TITLES = {
    "index":        "Hà Tĩnh Discovery — Khám phá Hà Tĩnh",
    "about":        "Giới thiệu — Hà Tĩnh Discovery",
    "destinations": "Điểm đến — Hà Tĩnh Discovery",
    "tours":        "Tour du lịch — Hà Tĩnh Discovery",
    "contact":      "Liên hệ — Hà Tĩnh Discovery",
    "news":         "Tin tức — Hà Tĩnh Discovery",
    "services":     "Dịch vụ — Hà Tĩnh Discovery",
}

CORE_PAGES = ["index", "about", "destinations", "tours", "contact", "news", "services"]


def replace_images(content):
    # Replace scraped full-path src="assets/.../images/FILENAME"
    for orig, new in IMG_SRC_MAP.items():
        content = content.replace(
            f'src="{ASSET_BASE}{orig}"',
            f'src="{SHARED}/{new}"'
        )
    # Fix scraper artifact: src="index.htmlimages/FILENAME" (missing slash)
    for orig, new in IMG_SRC_MAP.items():
        content = content.replace(
            f'src="index.htmlimages/{orig}"',
            f'src="{SHARED}/{new}"'
        )

    # Replace background-image url(images/FILENAME) inline styles
    for orig, new in BG_MAP.items():
        for fmt in [f'url(images/{orig})', f"url('images/{orig}')"]:
            content = content.replace(fmt, f'url({SHARED}/{new})')

    # Hero slider: 3 slides all reference home_slider.jpg — differentiate
    counter = [0]
    def _slide_replace(m):
        idx = min(counter[0], len(HERO_SLIDES) - 1)
        counter[0] += 1
        return f'background-image:url({SHARED}/{HERO_SLIDES[idx]})'
    content = re.sub(
        r'background-image:url\(images/home_slider\.jpg\)',
        _slide_replace,
        content,
    )

    # Force eager loading — off-screen lazy images don't render in screenshots
    content = content.replace(' loading="lazy"', ' loading="eager"')
    content = content.replace(' decoding="async"', ' decoding="sync"')
    return content


CONTRAST_FIX_CSS = """<style>
/* ha-tinh-ported */
.home .background_image,
.testimonials .background_image,
.travello .background_image,
footer .background_image,
.parallax_background {
  filter: brightness(0.55);
}
.page_header .background_image {
  filter: brightness(0.5);
}
.intro_background {
  display: none;
}
/* AOS: static render — force-show all animated elements */
[data-aos] {
  opacity: 1 !important;
  transform: none !important;
}
</style>"""


def replace_text(content, page="index"):
    # Remove tracker scripts (GTM / GA / Cloudflare)
    content = re.sub(
        r'<script[^>]*(googletagmanager|gtag|google_tags|cloudflare)[^>]*>.*?</script>',
        '', content, flags=re.DOTALL | re.IGNORECASE,
    )
    content = re.sub(
        r'\(function\(w,i,g\).*?google_tags.*?\}\);',
        '', content, flags=re.DOTALL,
    )
    # Remove colorlib preview analytics script
    content = re.sub(
        r'<script[^>]*s9cc[^>]*>.*?</script>',
        '', content, flags=re.DOTALL,
    )

    # Remove noindex added by colorlib preview
    content = content.replace('<meta name="robots" content="noindex, nofollow">', '')

    # Language
    content = content.replace('lang="en"', 'lang="vi"')

    # Page title
    content = re.sub(
        r'<title>.*?</title>',
        f'<title>{PAGE_TITLES.get(page, "Hà Tĩnh Discovery")}</title>',
        content,
    )

    # Meta description
    content = re.sub(
        r'(<meta name="description" content=")[^"]*(")',
        r'\1Khám phá Hà Tĩnh — biển Thiên Cầm, hồ Kẻ Gỗ, Ngã ba Đồng Lộc. Tour văn hóa và thiên nhiên thiết kế riêng cho từng du khách.\2',
        content,
    )

    # Fix index-1.html → index.html (scraper saved homepage as both)
    content = content.replace('href="index-1.html"', 'href="index.html"')
    content = content.replace("href='index-1.html'", "href='index.html'")

    # Brand
    content = re.sub(r'>Travello<', '>Hà Tĩnh Discovery<', content)
    content = content.replace('Travello - Travel &amp; Tourism Template', 'Hà Tĩnh Discovery')
    content = content.replace('Travello Travel', 'Hà Tĩnh Discovery')

    # Nav
    content = re.sub(r'>Home<',         '>Trang chủ<',        content)
    content = re.sub(r'>About us<',     '>Giới thiệu<',       content)
    content = re.sub(r'>About Us<',     '>Giới thiệu<',       content)
    content = re.sub(r'>Services<',     '>Dịch vụ<',          content)
    content = re.sub(r'>News<',         '>Tin tức<',          content)
    content = re.sub(r'>Contact<',      '>Liên hệ<',          content)
    content = re.sub(r'>Destinations<', '>Điểm đến<',         content)
    content = re.sub(r'>Tours<',        '>Tour<',              content)

    # Phone / contact
    content = content.replace('Call us: 00-56 445 678 33', 'Hotline: 0966 888 888')
    content = re.sub(r'00-56 445 678 33', '0966 888 888', content)

    # Hero slider texts
    content = content.replace('>Let us take you away<',  '>Khám phá Hà Tĩnh<')
    content = content.replace('>Discover the world<',    '>Biển xanh · Núi rừng · Di sản<')
    content = content.replace('>Adventure awaits<',      '>Hành trình bắt đầu từ đây<')

    # Search bar
    content = content.replace('>Search for your trip<', '>Tìm kiếm chuyến đi<')
    content = content.replace('placeholder="City"',      'placeholder="Điểm đến"')
    content = content.replace('placeholder="Departure"', 'placeholder="Ngày đi"')
    content = content.replace('placeholder="Arrival"',   'placeholder="Ngày về"')
    content = content.replace('placeholder="Budget"',    'placeholder="Ngân sách"')
    content = re.sub(r'>search<', '>Tìm kiếm<', content)

    # Section headings
    content = content.replace('>simply amazing places<',  '>những điểm đến tuyệt vời<')
    content = content.replace('>Popular Destinations<',   '>Điểm đến nổi bật<')
    content = content.replace('>Our Destinations<',       '>Điểm đến Hà Tĩnh<')
    content = content.replace('>Why Choose Us?<',         '>Tại sao chọn chúng tôi?<')
    content = content.replace('>Latest News<',            '>Tin tức mới nhất<')
    content = re.sub(r'>Testimonials<',                   '>Cảm nhận khách hàng<', content)
    content = content.replace('>Our Services<',           '>Dịch vụ của chúng tôi<')
    content = content.replace('>Our Team<',               '>Đội ngũ<')
    content = content.replace('>Get In Touch<',           '>Liên hệ với chúng tôi<')
    content = content.replace('>Send Message<',           '>Gửi tin nhắn<')
    content = content.replace('>Our Tours<',              '>Các chuyến tour<')
    content = content.replace('>Top Destinations<',       '>Điểm đến nổi bật<')
    content = content.replace('>The Best Prices<',        '>Giá tốt nhất<')
    content = content.replace('>Amazing Services<',       '>Dịch vụ tận tâm<')
    content = content.replace('>Fast Services<',          '>Phản hồi nhanh<')
    content = content.replace('>Special Offer<',          '>Ưu đãi<')

    # Side page nav labels
    content = content.replace('>Offers<',      '>Điểm đến<')
    content = content.replace('>Latest<',      '>Tin tức<')

    # Destination names (link text + alt)
    DESTS = [
        ("Bali",          "Biển Thiên Cầm"),
        ("Indonesia",     "Hồ Kẻ Gỗ"),
        ("San Francisco", "Chùa Hương Tích"),
        ("Paris",         "Ngã ba Đồng Lộc"),
        ("Phi Phi Island","Bãi Lữ"),
        ("Mykonos",       "Đèo Ngang"),
        ("Hawaii",        "Suối Tiên"),
        ("Maldives",      "Bãi Chánh"),
        ("New York",      "Vũng Áng"),
    ]
    for en, vi in DESTS:
        content = content.replace(f'>{en}<',       f'>{vi}<')
        content = content.replace(f'alt="{en}"',   f'alt="{vi}"')
        content = content.replace(f'title="{en}"', f'title="{vi}"')

    # Prices
    content = re.sub(r'From \$\d+',           'Từ 990.000đ',   content)
    content = re.sub(r'\$\d+\s*/\s*[Pp]erson','990.000đ/người',content)
    content = re.sub(r'>\$\d+(\.\d+)?<',      '>1.990.000đ<',  content)

    # Lorem ipsum placeholders → Vietnamese
    content = content.replace(
        'Nulla pretium tincidunt felis, nec.',
        'Điểm đến văn hóa và thiên nhiên độc đáo.'
    )
    content = content.replace(
        'Sollicitudin mauris lobortis in.',
        'Ưu đãi tour trọn gói, giá tốt nhất thị trường.'
    )
    content = re.sub(
        r'Quick booking confirmations and 24/7 customer support.*?anywhere\.',
        'Xác nhận đặt tour nhanh, hỗ trợ 24/7 trong suốt hành trình.',
        content,
    )

    # Tour cards
    TOURS = [
        ("Bali Adventure Explorer",   "Tour khám phá Thiên Cầm"),
        ("Paris Art &amp; Culture",   "Tour Di tích Đồng Lộc"),
        ("Thailand Island Hopping",   "Tour sinh thái hồ Kẻ Gỗ"),
        ("Greek Islands Discovery",   "Tour văn hóa Hương Tích"),
        ("Machu Picchu Trek",         "Tour trekking Đèo Ngang"),
        ("African Safari",            "Tour làng chài Thiên Cầm"),
    ]
    for en, vi in TOURS:
        content = content.replace(f'>{en}<', f'>{vi}<')
        content = content.replace(f'>{en}</a>', f'>{vi}</a>')

    TOUR_LOCS = [
        ("Bali, Indonesia",   "Thiên Cầm, Hà Tĩnh"),
        ("Paris, France",     "Đồng Lộc, Hà Tĩnh"),
        ("Thailand",          "Hồ Kẻ Gỗ, Hà Tĩnh"),
        ("Greece",            "Hương Tích, Hà Tĩnh"),
        ("Peru",              "Đèo Ngang, Hà Tĩnh"),
        ("Africa",            "Thiên Cầm, Hà Tĩnh"),
    ]
    for en, vi in TOUR_LOCS:
        content = content.replace(f'> {en}<', f'> {vi}<')

    # Tour descriptions → Vietnamese
    content = content.replace(
        'Experience the best of Bali with hiking, water sports, and cultural immersion.',
        'Khám phá biển Thiên Cầm — lặn ngắm san hô, câu cá, ẩm thực hải sản địa phương.'
    )
    content = content.replace(
        'Discover artistic treasures with guided tours of world-famous museums.',
        'Tham quan khu di tích Ngã ba Đồng Lộc — di sản lịch sử quốc gia, đầy cảm xúc.'
    )
    content = content.replace(
        'Explore stunning islands including Phi Phi, Koh Samui, and Phuket.',
        'Trải nghiệm hồ Kẻ Gỗ — kayak, câu cá, nghỉ dưỡng bên hồ giữa rừng xanh.'
    )
    content = content.replace(
        'Sail through the Cyclades visiting Mykonos, Santorini, and Naxos.',
        'Hành hương chùa Hương Tích và khám phá văn hóa tâm linh đặc sắc Hà Tĩnh.'
    )

    # Tour badges / buttons
    content = content.replace('>Best Seller<', '>Bán chạy<')
    content = content.replace('>View Details<', '>Xem chi tiết<')
    content = re.sub(r'>View All Tours<', '>Xem tất cả tour<', content)
    content = re.sub(r'>View All<', '>Xem tất cả<', content)

    # Tour durations
    content = re.sub(r'(\d+) Days', r'\1 Ngày', content)
    content = re.sub(r'(\d+) Nights', r'\1 Đêm', content)

    # Tour prices ($1,299 etc.) — round to nearest 100k VND, min 490k
    def _usd_to_vnd(m):
        usd = int(m.group().replace('$','').replace(',',''))
        if usd < 50:
            vnd = max(490000, round(usd * 20000 / 100000) * 100000)
        else:
            vnd = max(490000, round(usd * 800 / 100000) * 100000)
        return f'{vnd:,.0f}đ'
    content = re.sub(r'\$[\d,]+', _usd_to_vnd, content)
    # Fix wrong prices already in HTML (from old ×24 multiplier)
    content = content.replace('>31,176đ<',  '>1,490,000đ<')
    content = content.replace('>38,376đ<',  '>1,990,000đ<')
    content = content.replace('>52,776đ<',  '>2,490,000đ<')
    content = content.replace('>59,976đ<',  '>2,990,000đ<')
    content = content.replace('>43,176đ<',  '>1,690,000đ<')
    content = content.replace('>48,000đ<',  '>1,290,000đ<')

    # Instagram section
    content = content.replace('@Travello on Instagram', '@hatinhdiscovery')
    content = re.sub(r'>follow our journey<', '>theo dõi hành trình<', content)

    # News/blog
    content = re.sub(r'>Read More<', '>Đọc thêm<', content)
    content = re.sub(r'>View All News<', '>Xem tất cả tin tức<', content)

    # Form labels (contact page)
    content = content.replace('placeholder="Your Name"',    'placeholder="Họ và tên"')
    content = content.replace('placeholder="Your Email"',   'placeholder="Email"')
    content = content.replace('placeholder="Subject"',      'placeholder="Chủ đề"')
    content = content.replace('placeholder="Your Message"', 'placeholder="Nội dung"')
    content = re.sub(r'>Send Message<', '>Gửi tin nhắn<', content)
    content = re.sub(r'>Send<', '>Gửi<', content)

    # About page
    content = re.sub(r'>Our Story<', '>Câu chuyện của chúng tôi<', content)
    content = re.sub(r'>Our Mission<', '>Sứ mệnh<', content)
    content = re.sub(r'>Our Vision<', '>Tầm nhìn<', content)
    content = re.sub(r'>Happy Clients<', '>Khách hàng hài lòng<', content)
    content = re.sub(r'>Tours Completed<', '>Tour hoàn thành<', content)
    content = re.sub(r'>Countries Visited<', '>Tỉnh thành<', content)
    content = re.sub(r'>Awards Won<', '>Giải thưởng<', content)

    # About headings
    content = content.replace('>A few words about us<', '>Vài điều về chúng tôi<')
    content = re.sub(r'>read more<',  '>Xem thêm<', content, flags=re.IGNORECASE)
    content = content.replace('>Meet the Team<',         '>Đội ngũ chúng tôi<')
    content = content.replace('>Our History<',           '>Lịch sử phát triển<')
    content = content.replace('>The Beginning<',         '>Khởi đầu<')
    content = content.replace('>Award-Winning Service<', '>Dịch vụ đạt giải thưởng<')
    content = content.replace('>Digital Innovation<',    '>Đổi mới số hóa<')
    content = content.replace('>Global Expansion<',      '>Mở rộng kết nối<')
    content = content.replace('>Great Team<',            '>Đội ngũ chuyên nghiệp<')
    content = content.replace('>Watch Our Story<',       '>Xem câu chuyện của chúng tôi<')
    content = content.replace(
        "Watch how we've helped thousands of travelers explore the world",
        'Cùng chúng tôi khám phá vẻ đẹp thiên nhiên và văn hóa Hà Tĩnh'
    )
    content = content.replace(
        'We partner with the world\'s leading travel brands to bring you exceptional experiences and exclusive deals.',
        'Chúng tôi hợp tác với các đơn vị lữ hành địa phương uy tín để mang đến trải nghiệm khám phá Hà Tĩnh trọn vẹn nhất.'
    )

    # About page categories / filter tags
    content = content.replace('>Beach Resorts<',   '>Biển & Bãi tắm<')
    content = content.replace('>Cruise Lines<',    '>Tour thuyền<')
    content = content.replace('>Island Escapes<',  '>Nghỉ dưỡng<')
    content = content.replace('>Luxury Hotels<',   '>Khách sạn<')
    content = content.replace('>Photo Tours<',     '>Tour chụp ảnh<')
    content = content.replace('>Travel Finance<',  '>Thanh toán<')
    content = content.replace('>Best Deals<',      '>Ưu đãi<')
    content = content.replace('>Online Courses<',  '>Hướng dẫn<')

    # Team member names → Vietnamese names
    content = content.replace('>James Williams<',  '>Nguyễn Minh Khoa<')
    content = content.replace('>Margaret Smith<',  '>Trần Thị Lan Anh<')
    content = content.replace('>Michael James<',   '>Lê Văn Hùng<')
    content = content.replace('>Noah Smith<',      '>Phạm Thị Thu Hà<')

    # Stats labels
    content = content.replace('>Countries<',  '>Điểm đến<')
    content = content.replace('>Students<',   '>Học viên<')
    content = content.replace('>Teachers<',   '>Hướng dẫn viên<')

    # About page body - replace most visible Lorem ipsum with Vietnamese
    content = content.replace(
        'Pellentesque sit amet elementum ccumsan sit amet mattis eget, tristique at leo. Vivamus massa.Tempor massa et laoreet .Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed eu laoreet ante, sollicitudin volutpat quam. Vestibulum posuere malesuada ultrices. In pulvinar rhoncus lacus at aliquet. Nunc vitae lacus varius, auctor nisi sit amet, consectetur mauris. Curabitur sodales semper est, vel faucibus urna laoreet vel. Ut justo diam, sodales non pulvinar at, vulputate quis neque. Etiam aliquam purus vel ultricies consequat.',
        'Hà Tĩnh Discovery được thành lập với niềm đam mê giới thiệu vẻ đẹp thiên nhiên và văn hóa Hà Tĩnh đến du khách trong và ngoài nước. Từ bờ biển Thiên Cầm xanh ngắt đến hồ Kẻ Gỗ thơ mộng, từ khu di tích Ngã ba Đồng Lộc đến chùa Hương Tích linh thiêng — mỗi hành trình chúng tôi thiết kế đều mang đậm bản sắc địa phương và trải nghiệm chân thực.'
    )
    content = content.replace(
        'Pellentesque sit amet elementum ccumsan sit amet mattis eget, tristique at leo. Vivamus massa.Tempor massa et laoreet .Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
        'Chúng tôi tin rằng mỗi chuyến đi là một cơ hội để khám phá, học hỏi và kết nối với thiên nhiên và con người địa phương.'
    )
    content = content.replace(
        'Pellentesque sit amet elementum ccumsan sit amet mattis eget, tristique at leo. Vivamus massa.',
        'Hà Tĩnh Discovery — điểm khởi đầu cho hành trình khám phá xứ Nghệ.'
    )
    content = content.replace(
        'Pellentesque sit amet elementum ccumsan sit amet mattis eget, tristique at leo.',
        'Trải nghiệm văn hóa bản địa, ẩm thực địa phương và thiên nhiên nguyên sơ.'
    )
    content = content.replace(
        'Launched virtual tours during challenging times, keeping the spirit of travel alive. Introduced flexible booking policies and enhanced safety protocols.',
        'Ra mắt các tour khám phá hồ Kẻ Gỗ và biển Thiên Cầm với dịch vụ trọn gói, nhận được sự ủng hộ lớn từ du khách trong nước.'
    )

    # Timeline section
    content = content.replace('>10 Years of Creating Unforgettable Journeys<', '>10 Năm Tạo Nên Những Hành Trình Không Quên<')
    content = re.sub(r'>our journey<', '>hành trình của chúng tôi<', content)
    content = content.replace(
        'Travello was founded by a group of passionate travelers who wanted to share their love of exploration with the world. Starting with just 5 destinations, we began our journey.',
        'Hà Tĩnh Discovery được thành lập bởi những người yêu du lịch địa phương, bắt đầu với 5 tour khám phá Hà Tĩnh đầu tiên.'
    )
    content = content.replace(
        'We expanded our offerings to 50+ destinations across 4 continents. Our team grew to include local guides who brought authentic experiences to every tour.',
        'Mở rộng lên 20+ điểm đến khắp Hà Tĩnh với đội ngũ hướng dẫn viên địa phương nhiệt huyết và am hiểu văn hóa bản địa.'
    )
    content = content.replace(
        'Recognized as "Best Emerging Travel Agency" by Travel Weekly. We launched our popular adventure tour series and sustainability initiatives.',
        'Được công nhận "Đơn vị lữ hành tiêu biểu" tỉnh Hà Tĩnh. Ra mắt chuỗi tour phiêu lưu và sáng kiến du lịch xanh bền vững.'
    )
    content = content.replace(
        'Now serving 100+ destinations with over 50,000 happy travelers. We continue to innovate while staying true to our mission of creating unforgettable experiences.',
        'Phục vụ hơn 5.000 du khách mỗi năm, tiếp tục đổi mới để mang đến trải nghiệm Hà Tĩnh trọn vẹn và khó quên nhất.'
    )
    content = content.replace('>Today &amp; Beyond<', '>Hôm nay &amp; Tương lai<')
    content = content.replace('>Today & Beyond<',     '>Hôm nay & Tương lai<')

    # Featured Tours section
    content = content.replace('>curated experiences<', '>những tour nổi bật<')
    content = content.replace('>Featured Tours<', '>Tour Nổi Bật<')
    content = re.sub(r'<span class="price_from">From</span>', '<span class="price_from">Từ</span>', content)
    content = content.replace('>New<', '>Mới<')

    # Why section item 2 (Expert Guides)
    content = content.replace('>Expert Guides<', '>Hướng dẫn viên địa phương<')
    content = content.replace(
        'Our experienced local guides ensure authentic experiences and insider knowledge at every destination.',
        'Hướng dẫn viên địa phương am hiểu từng cung đường, từng làng chài — trải nghiệm chân thực, sâu sắc.'
    )
    content = content.replace(
        'Competitive prices with price-match guarantee. Quality travel experiences without breaking the bank.',
        'Giá cạnh tranh, cam kết tốt nhất thị trường. Trải nghiệm chất lượng không cần lo chi phí.'
    )

    # Testimonial quotes (Lorem ipsum placeholders)
    content = content.replace(
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit. lobortis dolor. Cras placerat lectus a posuere aliquet. Curabitur quis vehicula odio.',
        'Chuyến đi đến biển Thiên Cầm thực sự tuyệt vời! Hướng dẫn viên nhiệt tình, lịch trình hợp lý. Chắc chắn tôi sẽ quay lại!'
    )
    content = content.replace(
        'Praesent commodo cursus magna, vel scelerisque nisl consectetur et. Donec id elit non mi porta gravida at eget metus.',
        'Hồ Kẻ Gỗ đẹp hơn tôi tưởng rất nhiều. Tour sinh thái tổ chức bài bản, giá cả hợp lý. Cảm ơn đội ngũ Hà Tĩnh Discovery!'
    )
    content = content.replace(
        'Maecenas sed diam eget risus varius blandit sit amet non magna. Integer posuere erat a ante venenatis dapibus posuere velit aliquet.',
        'Tham quan khu di tích Ngã ba Đồng Lộc — xúc động và ý nghĩa sâu sắc. Đội ngũ hướng dẫn rất chuyên nghiệp và tận tâm.'
    )
    # Testimonial author names
    content = content.replace('>john turner,<', '>Nguyễn Văn Trung,<')
    content = content.replace('>client<', '>du khách<')
    content = content.replace('>sarah smith,<', '>Trần Thị Mai,<')
    content = content.replace('>traveler<', '>du khách<')
    content = content.replace('>mike johnson,<', '>Lê Minh Đức,<')
    content = content.replace('>adventurer<', '>phượt thủ<')
    # Testimonials sidebar nav
    content = content.replace('>City Breaks Clients<', '>Khách thành thị<')
    content = content.replace('>Cruises Clients<', '>Khách du thuyền<')
    content = content.replace('>All Inclusive Clients<', '>Khách trọn gói<')

    # News titles — all template items share same EN placeholder, vary them
    _news_titles = [
        'Khám phá Hà Tĩnh mùa hè này',
        'Top 5 điểm đến không thể bỏ qua',
        'Ẩm thực Hà Tĩnh — hương vị biển cả',
        'Hồ Kẻ Gỗ — thiên đường sinh thái',
        'Ngã ba Đồng Lộc — ký ức lịch sử',
        'Biển Thiên Cầm xanh ngắt mùa thu',
    ]
    _cnt = [0]
    def _next_news_title(m):
        t = _news_titles[min(_cnt[0], len(_news_titles) - 1)]
        _cnt[0] += 1
        return f'>{t}<'
    content = re.sub(r'>Best tips to travel light<', _next_news_title, content)
    content = content.replace('>lifestyle &amp; travel<', '>khám phá &amp; trải nghiệm<')
    content = content.replace('>lifestyle & travel<',    '>khám phá & trải nghiệm<')
    content = content.replace('>june<', '>tháng 6<')
    content = content.replace('>may<',  '>tháng 5<')
    content = content.replace('>april<', '>tháng 4<')

    # Cleanup remaining Lorem ipsum fragments (scraper leftovers in news posts)
    content = re.sub(r'\.?\s*Tempor massa et laoreet(?: malesuada)?\.?', '', content)
    content = re.sub(r'Vivamus massa\.\s*', '', content)
    content = re.sub(r'\s*Aliquam nulla nisl, accumsan sit amet mattis\.', '', content)

    # Discount promo box
    content = content.replace('>Get a 20% Discount<', '>Ưu đãi 20% khi đặt online<')
    content = content.replace('>Buy Your Vacation Online Now<', '>Đặt tour ngay hôm nay<')

    # Newsletter
    content = content.replace(
        'Subscribe to our newsletter to get the latest trends &amp; news',
        'Đăng ký nhận tin tức &amp; ưu đãi từ Hà Tĩnh Discovery'
    )
    content = content.replace(
        'Subscribe to our newsletter to get the latest trends & news',
        'Đăng ký nhận tin tức & ưu đãi từ Hà Tĩnh Discovery'
    )
    content = content.replace('>Join our database NOW!<', '>Cập nhật thông tin hành trình Hà Tĩnh<')
    content = content.replace('placeholder="Name"',       'placeholder="Họ tên"')
    content = content.replace('placeholder="Your e-mail"','placeholder="Email"')
    content = re.sub(r'>subscribe<', '>Đăng ký<', content)

    # Footer contact titles
    content = content.replace('>give us a call<',      '>Gọi cho chúng tôi<')
    content = content.replace('>come &amp; drop by<',  '>Địa chỉ văn phòng<')
    content = content.replace('>send us a message<',   '>Gửi email<')

    # Footer contact info
    content = content.replace('Office Landline: +44 5567 32 664 567', 'Văn phòng: 0239 388 8888')
    content = content.replace('Mobile: +44 5567 89 3322 332',         'Hotline: 0966 888 888')
    content = content.replace('4124 Barnes Street, Sanford, FL 32771','123 Đường Thiên Cầm, Kỳ Anh, Hà Tĩnh')
    content = content.replace('youremail@gmail.com',                  'info@hatinhdiscovery.vn')
    content = content.replace('Office@yourbusinessname.com',          'booking@hatinhdiscovery.vn')

    # Fix duplicated year: script writes year + static fallback year = "20262026"
    content = re.sub(r'(</script>)\d{4}(\s+All rights reserved)', r'\1\2', content)

    # Footer brand (only text nodes, not URL paths)
    content = re.sub(r'© (\d{4}) Colorlib', r'© \1 Hà Tĩnh Discovery', content)
    content = re.sub(r'Design: <a[^>]*>Colorlib</a>', 'Hà Tĩnh Discovery', content)

    return content


def port_page(page_name):
    path = os.path.join(DEMO_DIR, f"{page_name}.html")
    if not os.path.exists(path):
        print(f"  SKIP (not found): {page_name}.html")
        return
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    content = replace_images(content)
    content = replace_text(content, page_name)
    # Inject contrast-fix CSS before </head> (idempotent)
    if 'ha-tinh-ported' not in content:
        content = content.replace('</head>', CONTRAST_FIX_CSS + '\n</head>', 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  OK {page_name}.html")


REDIRECT_HTML = '<!DOCTYPE html><html><head><meta charset="UTF-8"><meta http-equiv="refresh" content="0; url=index.html"></head><body></body></html>'


if __name__ == "__main__":
    print("Porting Travello -> Ha Tinh Discovery...")
    for page in CORE_PAGES:
        port_page(page)
    # index-1.html is a scraper artifact — redirect to index
    with open(os.path.join(DEMO_DIR, "index-1.html"), "w", encoding="utf-8") as f:
        f.write(REDIRECT_HTML)
    print("  OK index-1.html (redirect)")
    print("Done.")
