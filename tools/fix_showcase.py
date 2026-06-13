#!/usr/bin/env python3
"""Infrastructure fixes: broken assets, vendor UI, crawl artifacts, EN cleanup."""
from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMG = "../assets/shared-images"

GLOBAL_HIDE = """<style id="showcase-cleanup">
.template-popup-wrapper,.showcase-dropdown-wrapper,.showcase-dropdown,.w-webflow-badge,.w-iframe-block,
a[href*="framer.com/templates"],[data-framer-name="Buy"],
.framer-badge,[class*="buy-template"],[data-framer-component-type="Badge"],
p:has(a[href*="framer.com"]):last-child{display:none!important;visibility:hidden!important}
</style>"""

MOONLIT_ICON_FALLBACK = """<style id="moonlit-icon-fallback">
[class^="flaticon-"]:before,[class*=" flaticon-"]:before{font-family:inherit!important;font-style:normal}
.flaticon-phone-flip:before{content:"📞"}
.flaticon-envelope:before{content:"✉"}
.flaticon-marker:before{content:"📍"}
.flaticon-calendar:before{content:"📅"}
.flaticon-user:before{content:"👤"}
.flaticon-people:before{content:"👥"}
.flaticon-construction:before{content:"📐"}
.flaticon-play:before{content:"▶"}
.flaticon-star:before,.flaticon-star-sharp-half-stroke:before{content:"★";color:#e9a225}
.flaticon-check-circle:before{content:"✓"}
</style>"""

SEASIDE_IMG_POOL = [
    "08_hospitality_hospitality_beachfront_resort.png",
    "35_hospitality_peaceful_beach_resort.png",
    "09_hospitality_hospitality_sea_view_room.png",
    "29_hospitality_luxury_sea_view_room.png",
    "60_hospitality_sea_view_room_bright.png",
    "16_hospitality_resort_infinity_pool_sunset.png",
    "48_hospitality_beach_resort_golden_hour.png",
    "26_hospitality_beach_restaurant_sunset.png",
]

MOONLIT_VI = [
    (r"Moonlit Hotel Ha Tinh(?:\s+Ha Tinh)+", "Moonlit Hotel Ha Tinh"),
    (r"Moonlit Hotel(?:\s+Hotel)+", "Moonlit Hotel Ha Tinh"),
    ("Moonlit Hotel Hotel Ha Tinh", "Moonlit Hotel Ha Tinh"),
    ("Moonlit Hotel Ha Tinh - Khách sạn Hà Tĩnh React Js Template", "Khách sạn hiện đại cho chuyến đi Hà Tĩnh"),
    ("Moonlit - Hotel and Resort React Js Template", "Khách sạn hiện đại cho chuyến đi Hà Tĩnh"),
    ("React Js Template", ""),
    (
        r"Welcome to Moonlit(?: Hotel Ha Tinh)?, where luxury meets comfort[^<]{0,320}",
        "Khách sạn hiện đại cho chuyến đi Hà Tĩnh",
    ),
    ("Welcome to Our Hotel", "Chào mừng đến Moonlit Hotel"),
    ("Welcome to Our Spa", "Trải nghiệm spa & nghỉ dưỡng"),
    ("Luxury Stay Hotel Experience Comfort &amp; Elegance", "Trải nghiệm lưu trú sang trọng tại Hà Tĩnh"),
    ("Lavish Getaway A Blend of Comfort &amp; Style", "Kỳ nghỉ ven biển Thiên Cầm"),
    ("A Perfect Fusion of Comfort and Elegance", "Hài hòa giữa tiện nghi và thanh lịch"),
    ("Choosing Moonlit was one of the best decisions", "Moonlit Hotel là lựa chọn lưu trú tin cậy"),
    ("Choosing Bokinn was one of the best decisions", "Moonlit Hotel là lựa chọn lưu trú tin cậy"),
    (">Home<", ">Trang chủ<"),
    ("Sign In", "Đăng nhập"),
    ("Sign Up", "Đăng ký"),
    ("Giới thiệu us", "Giới thiệu"),
    ("Giới thiệu Us", "Giới thiệu"),
    ("Liên hệ Us", "Liên hệ"),
    ("Room One", "Phòng 1"),
    ("Room Two", "Phòng 2"),
    ("Room Three", "Phòng 3"),
    ("Room Four", "Phòng 4"),
    ("Room Details", "Chi tiết phòng"),
    ("Room Style", "Kiểu phòng"),
    (">Service<", ">Dịch vụ<"),
    (">Event<", ">Sự kiện<"),
    ("Activities", "Hoạt động"),
    ("Blog Details", "Chi tiết bài viết"),
    ("Learn More", "Tìm hiểu thêm"),
    ("Facilities", "Tiện ích"),
    ("Hotel Facilities", "Tiện ích khách sạn"),
    ("Phòng and Suites", "Phòng & suite"),
    ("24-Hour Security", "An ninh 24/7"),
    ("Fitness Center", "Phòng gym"),
    ("Swimming Pool", "Hồ bơi"),
    ("Testimonial", "Đánh giá"),
    ("What Our Client Say", "Khách hàng nói gì"),
    ("Special Offers", "Ưu đãi"),
    ("Special Offer", "Ưu đãi"),
    ("Ưu đãis", "Ưu đãi"),
    ("Family Fun Package", "Gói gia đình"),
    ("Spa Retreat", "Gói spa"),
    ("Romantic Getaway", "Gói lãng mạn"),
    ("Instagram Post", "Bài Instagram"),
    ("Follow on&nbsp;Instagram", "Theo dõi Instagram"),
    ("Join Our Newsletter", "Nhận tin tức"),
    ("Quick Links", "Liên kết"),
    ("Guest Service", "Dịch vụ khách"),
    ("Room Service", "Phục vụ phòng"),
    ("Concierge Service", "Lễ tân"),
    ("Check Now", "Kiểm tra"),
    ("Select Date", "Chọn ngày"),
    ("Adult", "Người lớn"),
    ("Child", "Trẻ em"),
    ("1 Person", "1 người"),
    ("2 Person", "2 người"),
    ("1 Child", "1 trẻ"),
    ("Experience Staff", "Nhân viên giàu kinh nghiệm"),
    ("Welcome To Our Moonlit Hotel Ha Tinh Hotel &amp; Resort", "Chào mừng đến Moonlit Hotel Ha Tinh"),
    ("Welcome To Our Moonlit Hotel Ha Tinh &amp; Resort", "Chào mừng đến Moonlit Hotel Ha Tinh"),
    ("The Ritz-Carlton", "Phòng Deluxe"),
    ("Four Seasons Hotels", "Suite view biển"),
    ("Waldorf Astoria Hotels", "Phòng cao cấp"),
    ("Timberline Hideaway Hotel", "Phòng view rừng"),
    ("Rocky Ridge Room", "Phòng tiêu chuẩn"),
    ("Sarah Martinez", "Nguyễn Thu Hà"),
    ("COO of Apex Solutions", "Khách doanh nhân"),
    ("+12505550199", "0239 385 6789"),
    ("moonlit@gmail.com", "contact@moonlit.demo"),
    ("280 Augusta Avenue, M5T 2L9 Toronto, Hà Tĩnh", "Thiên Cầm, Hà Tĩnh"),
    ("M5T 2L9 Toronto, Hà Tĩnh", "Thiên Cầm, Hà Tĩnh"),
    ("Khám phá Room", "Xem phòng"),
    (">Pages<", ">Trang<"),
    (">Blog<", ">Tin tức<"),
    (">Gallery<", ">Thư viện ảnh<"),
    (">Dining<", ">Ẩm thực<"),
    (">Login<", ">Đăng nhập<"),
    (">Register<", ">Đăng ký<"),
    (">Room<", ">Phòng<"),
    ("Your Name", "Họ và tên"),
    ("Your Email", "Email của bạn"),
    ("Your Message", "Nội dung tin nhắn"),
    ("Subscribe", "Đăng ký nhận tin"),
    ("3 Person", "3 người"),
    ("4 Person", "4 người"),
    ("5 Person", "5 người"),
    ("6 Person", "6 người"),
    ("7 Person", "7 người"),
    ("8 Person", "8 người"),
    ("9 Person", "9 người"),
    ("Meet The Team", "Đội ngũ"),
    ("Our Team", "Đội ngũ"),
    ("Deluxe Room", "Phòng Deluxe"),
    ("The local amusement park", "Khu vui chơi Thiên Cầm"),
    ("Hotel Info Center", "Thông tin khách sạn"),
    ("Hotel location", "Vị trí khách sạn"),
    ("Apartment Hotel", "Khách sạn căn hộ"),
    ("Beach Hotel", "Khách sạn biển"),
    ("City Hotel", "Khách sạn thành phố"),
    ("Hotel Dark", "Giao diện tối"),
    ("Hotel Seaside", "Khách sạn ven biển"),
    ("Luxe Vista Hotel", "Luxe Vista"),
    ("LuxeVista Hotel", "LuxeVista"),
    ("Mountain Hotel", "Khách sạn núi"),
    ("Ocean Breeze Hotel", "Ocean Breeze"),
    ("Spa &amp; Wellness", "Spa & chăm sóc"),
    ("Spa & Wellness", "Spa & chăm sóc"),
    ("Spa & wellness", "Spa & chăm sóc"),
    ("Manage Preferences", ""),
    ("Cookies enable you to use shopping carts", ""),
    ("Cookie demo", ""),
    ("Login To Moonlit Hotel Ha Tinh", "Đăng nhập Moonlit Hotel"),
    ("Create A Free Account", "Tạo tài khoản"),
    ("Password", "Mật khẩu"),
    ("Remember me", "Ghi nhớ đăng nhập"),
    (">Or<", ">Hoặc<"),
    (" we've ever made. They have proven to be a reliable and innovative partner", " tại Hà Tĩnh."),
    ("Hotel Tiện ích", "Tiện ích khách sạn"),
    ("Varied types of rooms, from standard to luxury suites, equipped with essentials like beds.", "Nhiều loại phòng từ tiêu chuẩn đến suite, đầy đủ tiện nghi."),
    ("Our Phòng", "Phòng nghỉ"),
    (
        r"Our rooms offer[\s\S]{0,220}?every guest\.",
        "Phòng nghỉ tiện nghi, thiết kế thanh lịch cho mọi khách.",
    ),
    (
        r"On-site security personnel and best surveillance\.[\s\S]{0,120}?valuables\.",
        "An ninh 24/7 và kho an toàn cho hành trang.",
    ),
    (
        r"Equipped with exercise machines and weights\.[\s\S]{0,120}?treatments\.",
        "Phòng gym và spa với dịch vụ massage, chăm sóc da.",
    ),
    (
        r"Indoor or outdoor pools for leisure or exercise\.[\s\S]{0,100}?treatments",
        "Hồ bơi trong nhà và ngoài trời phục vụ thư giãn.",
    ),
    ("15% off on family suites", "Giảm 15% suite gia đình"),
    ("Free meals for kids under 12", "Miễn phí bữa ăn trẻ dưới 12 tuổi"),
    ("Complimentary tickets", "Vé tham quan miễn phí"),
    ("A two-night stay in a room", "Lưu trú hai đêm"),
    ("Daily spa treatments", "Spa mỗi ngày"),
    ("Healthy breakfast and lunch", "Bữa sáng và trưa đầy đủ dinh dưỡng"),
    ("Access to all spa", "Sử dụng toàn bộ khu spa"),
    ("Enter your mail", "Nhập email"),
    ("+1234567890", "0239 385 6789"),
    ("info@hostie.com", "contact@moonlit.demo"),
    ("Chi tiết phòng One", "Chi tiết phòng 1"),
    ("Chi tiết phòng Two", "Chi tiết phòng 2"),
    ("Room Dịch vụ", "Phục vụ phòng"),
    ("Concierge Dịch vụ", "Lễ tân"),
    ("24/7 Front Desk", "Lễ tân 24/7"),
    ("Parking", "Bãi đỗ xe"),
    ("Free Wi-Fi", "Wi-Fi miễn phí"),
    ("Phòng & Suites", "Phòng & suite"),
    (
        r"Each room features plush bedding, high-quality linens, and a selection of[\s\S]{0,120}?sleep\.",
        "Phòng ngủ êm ái với ga gối cao cấp.",
    ),
    ("Moonlit Hotel Ha Tinh@gmail.com", "contact@moonlit.demo"),
    ("OceanBreeze Resort", "Ocean Breeze"),
    ("LuxeVista", "Luxe Vista"),
    ("1 Trẻ em", "1 trẻ"),
    ("2 Trẻ em", "2 trẻ"),
    ("100$", "2.500.000đ"),
    ("130$", "3.200.000đ"),
    ("150$", "3.800.000đ"),
    ("$39.00", "990.000đ"),
    ("Powered by Colorlib", ""),
    ("Designed by Colorlib", ""),
]

COLORLIB_IMG = {
    "images/bg_1.jpg": f"{IMG}/08_hospitality_hospitality_beachfront_resort.png",
    "images/bg_2.jpg": f"{IMG}/17_hospitality_modern_beach_hotel_exterior.png",
    "images/room-1.jpg": f"{IMG}/09_hospitality_hospitality_sea_view_room.png",
    "images/room-2.jpg": f"{IMG}/29_hospitality_luxury_sea_view_room.png",
    "images/room-3.jpg": f"{IMG}/60_hospitality_sea_view_room_bright.png",
    "images/room-4.jpg": f"{IMG}/45_hospitality_luxury_seaside_hotel_room.png",
    "images/room-5.jpg": f"{IMG}/35_hospitality_peaceful_beach_resort.png",
    "images/room-6.jpg": f"{IMG}/48_hospitality_beach_resort_golden_hour.png",
    "images/person_1.jpg": f"{IMG}/54_lifestyle_friends_beach_walk_sunset.png",
    "images/person_2.jpg": f"{IMG}/14_lifestyle_group_travelers_beach_sunset.png",
    "images/person_3.jpg": f"{IMG}/10_experience_experience_ke_go_boat_tour.png",
    "images/food-1.jpg": f"{IMG}/26_hospitality_beach_restaurant_sunset.png",
    "images/food-2.jpg": f"{IMG}/40_hospitality_seaside_restaurant_sunset.png",
}
for i in range(1, 7):
    COLORLIB_IMG[f"images/insta-{i}.jpg"] = f"{IMG}/{'08_hospitality_hospitality_beachfront_resort.png' if i % 2 else '35_hospitality_peaceful_beach_resort.png'}"
for i in range(1, 8):
    COLORLIB_IMG[f"images/image_{i}.jpg"] = f"{IMG}/09_hospitality_hospitality_sea_view_room.png"
COLORLIB_IMG["images/about.jpg"] = f"{IMG}/17_hospitality_modern_beach_hotel_exterior.png"
for i in range(1, 9):
    COLORLIB_IMG[f"images/menu-{i}.jpg"] = f"{IMG}/{'26_hospitality_beach_restaurant_sunset.png' if i % 2 else '40_hospitality_seaside_restaurant_sunset.png'}"

COLORLIB_VI = [
    ("Chào mừng To Deluxe Hotel Ha Tinh", "Lựa chọn lưu trú tiện nghi tại Hà Tĩnh"),
    ("Chào mừng to Deluxe Hotel Ha Tinh Khách sạn", "Deluxe Hotel Ha Tinh"),
    ("Chào mừng To Our Khách sạn", "Chào mừng đến Deluxe Hotel Ha Tinh"),
    ("Enjoy A Tiện nghi Experience", "Trải nghiệm lưu trú tiện nghi"),
    ("Join With Us", "Đặt phòng ngay"),
    ("Liên hệ Us", "Liên hệ"),
    ("Liên hệ Information", "Thông tin liên hệ"),
    ("Our Phòng", "Phòng nghỉ"),
    ("Tiện nghi Room", "Phòng tiêu chuẩn"),
    ("Happy Guests", "Khách hàng"),
    ("Staffs", "Nhân viên"),
    ("Guests", "Khách"),
    ("Check-in Date", "Ngày nhận phòng"),
    ("Check-out Date", "Ngày trả phòng"),
    ("Check-in date", "Ngày nhận phòng"),
    ("Check-out date", "Ngày trả phòng"),
    ("View Room Details", "Xem chi tiết phòng"),
    ("per night", "/ đêm"),
    ("Our Menu", "Thực đơn"),
    ("Our Restaurants", "Nhà hàng"),
    ("Send Message", "Gửi tin nhắn"),
    ("Your Email", "Email của bạn"),
    ("Your Name", "Họ và tên"),
    ("Enter message...", "Nhập nội dung..."),
    ("Have a Questions?", "Cần hỗ trợ?"),
    ("Address:", "Địa chỉ:"),
    ("Phone:", "Điện thoại:"),
    ("Email:", "Email:"),
    ("Privacy", "Riêng tư"),
    ("Services", "Dịch vụ"),
    ("Instagram", "Instagram"),
    ("Menu", "Menu"),
    ("Suite Room", "Phòng Suite"),
    ("Family Room", "Phòng gia đình"),
    ("Classic Room", "Phòng cổ điển"),
    ("Superior Room", "Phòng Superior"),
    ("Standard Room", "Phòng tiêu chuẩn"),
    ("Deluxe Room", "Phòng Deluxe"),
    ("1 Adult", "1 người lớn"),
    ("2 Adult", "2 người lớn"),
    ("Customer", "Khách"),
    ("Room", "Phòng"),
    ("$120.00", "2.950.000đ"),
    ("$20.00", "490.000đ"),
    ("$150.00", "3.700.000đ"),
    ("$130.00", "3.200.000đ"),
    ("$300.00", "7.400.000đ"),
    ("$500.00", "12.300.000đ"),
    ("198 West 21th Street, Suite 721 New York NY 10016", "Thiên Cầm, Hà Tĩnh"),
    ("203 Fake St. Mountain View, San Francisco, California, USA", "Thiên Cầm, Hà Tĩnh"),
    ("info@yourdomain.com", "contact@deluxe.demo"),
    ("+2 392 3929 210", "0239 385 6789"),
    ("This template is made with", ""),
    ("by Colorlib", ""),
    ("lang=\"vi\" lang=\"en\"", 'lang="vi"'),
    ("A small river named Duden flows by their place and supplies.", "Dịch vụ chu đáo cho khách lưu trú."),
    ("A small river named Duden flows by their place and supplies it with the necessary regelialia. It is a paradisematic country, in which roasted parts of sentences fly into your mouth.", "Khách sạn Deluxe mang đến trải nghiệm nghỉ dưỡng thoải mái tại Thiên Cầm."),
    ("When she reached the first hills of the Italic Mountains", "Deluxe Hotel Ha Tinh"),
    ("Nathan Smith", "Nguyễn Văn An"),
    ("25/7 Front Desk", "Lễ tân 24/7"),
    ("Restaurant Bar", "Nhà hàng & bar"),
    ("Transfer Dịch vụ", "Đưa đón sân bay"),
    ("Spa Suites", "Spa & suite"),
    ("Amenities", "Tiện ích"),
    ("Gift Card", "Thẻ quà tặng"),
    ("Career", "Tuyển dụng"),
    ("Useful Links", "Liên kết"),
    ("Recent Blog", "Tin mới"),
    ("Far far away, behind the word mountains", "Khách sạn tiện nghi ven biển Thiên Cầm"),
    ("3 Adult", "3 người lớn"),
    ("4 Adult", "4 người lớn"),
    ("5 Adult", "5 người lớn"),
    ("6 Adult", "6 người lớn"),
    ("Deluxe Hotel Ha Tinh Phòng", "Phòng Deluxe"),
    ("lang=\"en\" lang=\"vi\"", 'lang="vi"'),
]

HOTALE_UPLOAD_MAP = {
    "upload/Square.png": f"{IMG}/08_hospitality_hospitality_beachfront_resort.png",
    "upload/Group-36.jpg": f"{IMG}/35_hospitality_peaceful_beach_resort.png",
    "upload/grey-color.jpg": f"{IMG}/17_hospitality_modern_beach_hotel_exterior.png",
    "upload/home-resort-news-bg.png": f"{IMG}/48_hospitality_beach_resort_golden_hour.png",
    "upload/home-resort-newsletter-bg.png": f"{IMG}/29_hospitality_luxury_sea_view_room.png",
    "upload/footer-banner.png": f"{IMG}/48_hospitality_beach_resort_golden_hour.png",
    "upload/footer-cards.png": f"{IMG}/08_hospitality_hospitality_beachfront_resort.png",
    "upload/logo-resort.png": f"{IMG}/08_hospitality_hospitality_beachfront_resort.png",
    "upload/logo-nx1.png": f"{IMG}/08_hospitality_hospitality_beachfront_resort.png",
    "upload/logo-nx2-1.png": f"{IMG}/08_hospitality_hospitality_beachfront_resort.png",
}

ASATHA_IMG_POOL = [
    "18_hero_ke_go_lake_misty_morning.png",
    "19_hospitality_forest_lake_lodge.png",
    "20_hospitality_villa_infinity_pool_sunset.png",
    "58_hospitality_beach_villa_twilight_pool.png",
    "28_hospitality_resort_pool_evening.png",
    "57_hospitality_lake_resort_village.png",
    "26_hospitality_beach_restaurant_sunset.png",
    "59_hospitality_seaside_dining_balcony.png",
    "38_hospitality_quiet_lake_resort.png",
    "30_hospitality_lake_lodge_hatinh.png",
]

ASATHA_HIDE = """<style id="asatha-hide-vendor">.footer-copyright-div,.copyright-flowcub-text{display:none!important}</style>"""

TRAVOL_DEST_IMGS = [
    "04_destination_destination_ke_go_lake.png",
    "05_destination_destination_huong_tich_pagoda.png",
    "06_destination_destination_dong_loc_memorial.png",
    "12_destination_coastal_road_mountain_sea.png",
    "13_destination_fishing_boats_sunset_bay.png",
    "23_culture_traditional_market_hatinh.png",
]

TRAVOL_GALLERY_IMGS = [
    "02_hero_hero_coastal_beach_morning.png",
    "31_destination_coastal_road_overlook.png",
    "33_destination_fishing_harbor_sunset.png",
    "37_hero_lake_boat_landscape.png",
    "41_hero_quiet_lake_sunrise.png",
    "53_destination_coastal_harbor_golden_hour.png",
]

TRAVOL_BLOG_IMGS = [
    "07_experience_experience_local_seafood.png",
    "10_experience_experience_ke_go_boat_tour.png",
    "21_experience_kayak_lake_mountain_forest.png",
    "22_experience_seafood_table_beach.png",
    "44_experience_seafood_dinner_beach.png",
    "50_culture_fresh_local_market.png",
]

TRAVOL_TEAM_IMGS = [
    "14_lifestyle_group_travelers_beach_sunset.png",
    "27_lifestyle_couple_beach_walk_sunset.png",
    "50_culture_fresh_local_market.png",
]

TRAVOL_AVATAR_IMGS = [
    "27_lifestyle_couple_beach_walk_sunset.png",
    "54_lifestyle_friends_beach_walk_sunset.png",
    "14_lifestyle_group_travelers_beach_sunset.png",
]

TRAVOL_HIDE_CLIENTS = """<style id="travol-hide-clients">section.clients{display:none!important}</style>"""

FRAMER_VI = [
    ("Điểm đếns", "điểm đến"),
    ("Khám phárs", "khách"),
    ("Khám phár", "khách"),
    ("Khám phá Seekers", "Điểm đến mạo hiểm"),
    ("First-Time du khách", "Du khách lần đầu"),
    ("Eco-Friendly du khách", "Du khách thân thiện môi trường"),
    ("Khám phá Tour", "Tour khám phá"),
    ("We Craft Khám phás", "Chúng tôi thiết kế tour"),
    ("Khám phá trips", "Các chuyến đi"),
    ("Khám phá the charm", "Khám phá vẻ đẹp"),
    ("Khám phá the beauty", "Khám phá vẻ đẹp"),
    ("Khám phá the mystery", "Khám phá vẻ đẹp"),
    ("Khám phá the world", "Khám phá thế giới"),
    ("Khám phá New Horizons", "Khám phá điểm đến mới"),
    ("Start Your Khám phá Today", "Bắt đầu hành trình hôm nay"),
    ("Your Dream Island Khám phá", "Khám phá đảo mơ ước"),
    ("KHÁM PHÁ AWAITS", "HÀNH TRÌNH ĐANG CHỜ"),
    ("Bản demo , , designers and agencies.", ""),
    ("Designed by Fourtwelve", ""),
    ("Create a free website with", ""),
    ("the website builder loved by startups", ""),
    ("Book a Trip Now", "Đặt tour ngay"),
    ("Bắt đầu hành trình", "Bắt đầu hành trình"),
    ("Pricing", "Bảng giá"),
    ("FOLLOW US", "Theo dõi"),
    ("info@example.com", "contact@wander.demo"),
    ("+1 (555) 123-4567", "0239 385 6789"),
    ("123 Main Street, Suite 62704", "Thiên Cầm, Hà Tĩnh"),
    ("Travel and Tourism  Template", "Du lịch Hà Tĩnh"),
    ("Travel and Tourism Template", "Du lịch Hà Tĩnh"),
    (
        "is a premium Travel and Tourism  Template designed for agencies and explorers. "
        "Perfect for presenting destinations, travel experiences, and tourism services with modern design, "
        "smooth navigation, and global appeal.",
        "— công ty du lịch Hà Tĩnh, tour và trải nghiệm địa phương.",
    ),
    ("Wander Hà Tĩnh - Travel and Tourism  Template", "Wander Hà Tĩnh — Du lịch Hà Tĩnh"),
    ("About Our Values", "Giá trị của chúng tôi"),
    ("Tourists Reviews", "Đánh giá khách"),
    ("View Services", "Xem dịch vụ"),
    ("Adventure Tours", "Tour mạo hiểm"),
    ("Popular Tours", "Tour phổ biến"),
    ("About Company", "Giới thiệu công ty"),
    ("Tour details", "Chi tiết tour"),
    ("South America", "Miền Nam Hà Tĩnh"),
    ("North America", "Miền Bắc Hà Tĩnh"),
    ("Australia", "Ven biển"),
    ("Africa", "Núi rừng"),
    ("Asia", "Miền Trung"),
    ("Spain", "Thiên Cầm"),
    ("Cuba", "Kẻ Gỗ"),
    ("Egypt", "Hương Tích"),
    ("Indonesia", "Đồng Lộc"),
    ("Moonlit Hotel Ha Tinh Ha Tinh", "Moonlit Hotel Ha Tinh"),
]

MOUNTAIN_VI = [
    ("Ke Go Eco Eco Lodge", "Ke Go Eco Lodge"),
    ("Mountain Eco Lodge", "Ke Go Eco Lodge"),
    ("Your idyllic weekend retreat", "Chạm vào nhịp sống xanh bên hồ Kẻ Gỗ"),
    ("Tranquil Escape", "Nghỉ dưỡng an yên"),
    ("BOOK YOUR STAY", "ĐẶT PHÒNG"),
    ("Book your stay", "Đặt phòng"),
    ("OUR ROOMS", "PHÒNG NGHỈ"),
    (">ROOMS<", ">Phòng<"),
    (">RESTAURANT<", ">Nhà hàng<"),
    ("RESTAURANT &amp; BAR", "NHÀ HÀNG &amp; BAR"),
    ("Restaurants &amp; Bar", "Nhà hàng &amp; bar"),
    (">GALLERY<", ">Gallery<"),
    (">CONTACT<", ">Liên hệ<"),
    (">AREA<", ">Khu vực<"),
    (">EVENTS<", ">Sự kiện<"),
    (">DINING<", ">Ẩm thực<"),
    (">DISCOVER<", ">Khám phá<"),
    (">EXPLORE<", ">Khám phá<"),
    ("LEARN MORE", "TÌM HIỂU THÊM"),
    ("Learn more", "Tìm hiểu thêm"),
    ("AMENITIES AND FACILITIES", "TIỆN ÍCH &amp; DỊCH VỤ"),
    ("WHERE TO FIND US", "ĐỊA CHỈ"),
    ("LET'S STAY IN TOUCH", "GIỮ LIÊN LẠC"),
    ("SUBSCRIBE", "ĐĂNG KÝ"),
    ("PRIVACY POLICY", "CHÍNH SÁCH BẢO MẬT"),
    ("TERMS &amp; CONDITIONS", "ĐIỀU KHOẢN"),
    ("LICENSING", "GIẤY PHÉP"),
    ("Savour Culinary Excellence", "Thưởng thức ẩm thực địa phương"),
    ("Experience cosy quarters and stylish decor", "Không gian ấm cúng giữa thiên nhiên Kẻ Gỗ"),
    ("Get inspired", "Cảm hứng du lịch"),
    ("Conference rooms", "Phòng hội nghị"),
    ("Fitness center", "Phòng gym"),
    ("Room service", "Dịch vụ phòng"),
    ("Parking", "Bãi đỗ xe"),
    ("Reception 24/7", "Lễ tân 24/7"),
    ("Security 24/7", "An ninh 24/7"),
    ("Pottery class", "Lớp gốm thủ công"),
    ("Trekking tour", "Tour trekking"),
    ("Wine tasting", "Thử rượu vang"),
    ("Wholesome food", "Ẩm thực lành mạnh"),
    ("Arcosa, Italy", "Kẻ Gỗ, Hà Tĩnh"),
    ("Via Milioni 15,", "Thôn Kẻ Gỗ,"),
    ("For reservations,", "Đặt phòng:"),
    ("For any PR enquiries,", "Liên hệ báo chí:"),
    ("E-mail", "Email"),
    ("Framer template for a boutique hotel", "Eco lodge ven hồ Kẻ Gỗ — Hà Tĩnh"),
    ("Framer template page for a boutique hotel", "Eco lodge ven hồ Kẻ Gỗ — Hà Tĩnh"),
    ("BOUTIQUE HOTELS - AWARDS -", "ECO LODGE — HÀ TĨNH"),
    ("EVENTS &amp; WORKSHOPS", "SỰ KIỆN &amp; WORKSHOP"),
    ("nature sights", "cảnh thiên nhiên"),
    ("booking@mountainlodge.com", "datphong@kego.demo"),
    ("pr@mountainlodge.com", "lienhe@kego.demo"),
    ("please contact:", "liên hệ:"),
    ("ASCENT", "LEO NÚI"),
    ("Pavilion", "Sân hiên"),
    ("rooms", "phòng"),
]

LUXESTAY_VI = [
    (">Contact<", ">Liên hệ<"),
    (">Rooms<", ">Phòng<"),
    (">Restaurant<", ">Ẩm thực<"),
    (">About<", ">Giới thiệu<"),
    ("Contact us", "Liên hệ"),
    ("Luxestay", "LuxeStay Ha Tinh"),
    ("luxestay", "LuxeStay Ha Tinh"),
    ("The timeless luxury of island living", "Không gian nghỉ dưỡng riêng tư tại Hà Tĩnh"),
    ("Stay.  Explore.  Feel alive", "Ở lại. Khám phá. Tận hưởng Hà Tĩnh"),
    ("Book a stay", "Xem villa"),
    ("Everything you need for a perfect island stay", "Mọi thứ cho kỳ nghỉ trọn vẹn tại Hà Tĩnh"),
    ("Every room, a sanctuary of its own", "Mỗi phòng là một không gian riêng tư"),
    ("Experiences designed for living", "Trải nghiệm thiết kế cho nhịp sống thong dong"),
    ("Curated Island Activities", "Hoạt động được tuyển chọn"),
    ("Beach / Lagoon Access", "Gần biển &amp; hồ"),
    ("Garden or Ocean Views", "View vườn hoặc biển"),
    ("Infinity Pool", "Hồ bơi vô cực"),
    ("Meditation Spaces", "Không gian thiền"),
    ("Standard room", "Phòng tiêu chuẩn"),
    ("Celebrate Love", "Kỷ niệm tình yêu"),
    (">Wellness<", ">Spa<"),
    (">Wedding<", ">Tiệc cưới<"),
    (">Weddings<", ">Tiệc cưới<"),
    (">Dining<", ">Ẩm thực<"),
    (">Dine<", ">Ẩm thực<"),
    ("Explore more", "Xem thêm"),
    ("View more", "Xem thêm"),
    ("Follow us on", "Theo dõi"),
    ("Have any doubts?", "Cần tư vấn?"),
    ("Relax &amp; Renew", "Thư giãn &amp; tái tạo"),
    ("Taste &amp; Indulge", "Thưởng thức &amp; tận hưởng"),
    ("Location", "Vị trí"),
    ("Email", "Email"),
    ("Tel", "Điện thoại"),
    ("Created by uxridham", ""),
    ("uxridham@gmail.com", "contact@luxestay.demo"),
    ("Boardly.com", ""),
    ("Homing.com", ""),
    ("Expedra", ""),
    ("Tripscout", ""),
    ("LuxeStay Ha Tinh - Framer Template", "LuxeStay Ha Tinh — Villa Hà Tĩnh"),
    ("LuxeStay — Framer Template", "LuxeStay Ha Tinh — Villa Hà Tĩnh"),
]

MOUNTAIN_IMG_POOL = [
    "18_hero_ke_go_lake_misty_morning.png",
    "56_hero_misty_forest_lake_boat.png",
    "19_hospitality_forest_lake_lodge.png",
    "30_hospitality_lake_lodge_hatinh.png",
    "57_hospitality_lake_resort_village.png",
    "21_experience_kayak_lake_mountain_forest.png",
    "55_lifestyle_couple_lake_dock_sunset.png",
]

LUXESTAY_IMG_POOL = [
    "15_hospitality_luxury_resort_pool_sunset.png",
    "20_hospitality_villa_infinity_pool_sunset.png",
    "58_hospitality_beach_villa_twilight_pool.png",
    "38_hospitality_quiet_lake_resort.png",
    "29_hospitality_luxury_sea_view_room.png",
    "45_hospitality_luxury_seaside_hotel_room.png",
    "48_hospitality_beach_resort_golden_hour.png",
]

FRAMER_HIDE = """<style id="framer-hide-vendor">
#__framer-editorbar-container,#__framer-editorbar,.framer-1v1xq0x,
#__framer-badge-container,.framer-badge,a[href*="framer.com/edit"]{display:none!important;visibility:hidden!important}
</style>"""

VENDOR_STRIP = [
    ("Powered by Webflow", ""),
    ("Powered by&nbsp;Webflow", ""),
    ("Made by Flowcub", ""),
    ("Made by design.", ""),
    ("More Templates", ""),
    ("Style Guide", ""),
    ("Changelog", ""),
    ("Licenses", ""),
    ("Webflow", ""),
    ("Colorlib", ""),
    ("DuruThemes", ""),
    ("Max-Themes", ""),
    ("Framer", ""),
]


def p(name: str) -> str:
    return f"{IMG}/{name}"


def inject_head(html: str, snippet: str, marker: str) -> str:
    if marker in html:
        return html
    return html.replace("</head>", snippet + "</head>", 1)


def fix_crawl_artifacts(html: str) -> str:
    html = html.replace("index.htmlassets/", "assets/")
    html = html.replace("index.htmljs/", "assets/preview.colorlib.com/theme/deluxe/js/")
    return html


SEASIDE_WEBFLOW = "assets/assets.website-files.com/"
SEASIDE_STARS = (
    "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='96' height='16'%3E"
    "%3Ctext y='14' font-size='14' fill='%23e8b923'%3E%E2%98%85%E2%98%85%E2%98%85%E2%98%85%3C/text%3E%3C/svg%3E"
)
SEASIDE_RATING_CLASSES = (
    "featured-rating-image",
    "visitor-review-image",
    "room-overview-rating-image",
)


def _seaside_is_icon(src: str) -> bool:
    s = src.lower()
    return "icon-" in s or "/icon" in s or "favicon" in s or "webclip" in s


def _seaside_restore_paths(html: str) -> str:
    return html.replace("assets/cdn.prod.website-files.com/", SEASIDE_WEBFLOW)


def fix_seaside_rating(html: str) -> str:
    for cls in SEASIDE_RATING_CLASSES:
        html = re.sub(
            rf'(<img\b[^>]*class="[^"]*{cls}[^"]*"[^>]*src=")[^"]+(")',
            rf"\1{SEASIDE_STARS}\2",
            html,
        )
        html = re.sub(
            rf'(<img\b[^>]*src=")[^"]+("[^>]*class="[^"]*{cls}[^"]*")',
            rf"\1{SEASIDE_STARS}\2",
            html,
        )
    return html


def fix_seaside_imgs(html: str) -> str:
    html = _seaside_restore_paths(html)
    idx = 0

    def next_img() -> str:
        nonlocal idx
        path = p(SEASIDE_IMG_POOL[idx % len(SEASIDE_IMG_POOL)])
        idx += 1
        return path

    def img_repl(m: re.Match) -> str:
        tag = m.group(0)
        src = m.group(1)
        if _seaside_is_icon(src):
            return tag
        if any(c in tag for c in SEASIDE_RATING_CLASSES):
            return tag
        if src.endswith(".svg"):
            return tag
        return f'src="{next_img()}"'

    wf_img = (
        r'(?:assets/)?(?:cdn\.prod\.website-files\.com|assets\.website-files\.com)/[^"]+'
        r"\.(?:jpg|jpeg|png|webp)"
    )
    html = re.sub(rf'src="({wf_img})"', img_repl, html, flags=re.I)
    html = re.sub(
        rf'\s+srcset="(?:assets/)?(?:cdn\.prod\.website-files\.com|assets\.website-files\.com)/[^"]*"',
        "",
        html,
        flags=re.I,
    )

    def url_repl(m: re.Match) -> str:
        url = m.group(2)
        if _seaside_is_icon(url) or url.endswith(".svg"):
            return m.group(0)
        return f"url('{next_img()}')"

    html = re.sub(
        r"url\((['\"]?)(?:\.\./)*(?:assets/)?"
        r"(?:cdn\.prod\.website-files\.com|assets\.website-files\.com)/([^'\")\s]+)\1\)",
        url_repl,
        html,
        flags=re.I,
    )

    def json_url_repl(_m: re.Match) -> str:
        return f'"url": "{next_img()}"'

    html = re.sub(
        r'"url":\s*"(?:assets/)?(?:cdn\.prod\.website-files\.com|assets\.website-files\.com)/'
        r'[^"]+\.(?:jpg|jpeg|png|webp)"',
        json_url_repl,
        html,
        flags=re.I,
    )
    return fix_seaside_rating(html)


def fix_colorlib(html: str) -> str:
    for old, new in COLORLIB_VI:
        html = html.replace(old, new)
    html = re.sub(
        r"On her way she met a copy\.[\s\S]{0,800}?safe country\.",
        "Nhà hàng Deluxe Hotel phục vụ hải sản và đặc sản Hà Tĩnh trong không gian ven biển Thiên Cầm.",
        html,
    )
    html = re.sub(r"Little Blind Text", "nội dung demo", html)
    html = re.sub(r"Lorem ipsum[^<]{0,400}", "Nội dung demo phù hợp khách sạn Hà Tĩnh.", html)
    html = re.sub(
        r"Even the all-powerful Pointing has no control[^<]{0,200}",
        "Tin tức và ưu đãi tại Deluxe Hotel Ha Tĩnh.",
        html,
    )
    for old, new in COLORLIB_IMG.items():
        html = html.replace(old, new)
        html = html.replace(f"url({old})", f"url({new})")
    html = html.replace(
        "assets/preview.colorlib.com/theme/deluxe/../assets/shared-images/",
        "../assets/shared-images/",
    )
    html = re.sub(
        r'<script[^>]*preview\.colorlib\.com/s9cc[^>]*></script>',
        "",
        html,
        flags=re.I,
    )
    html = re.sub(
        r'<script[^>]*jquery\.timepicker\.min\.js[^>]*></script>',
        "",
        html,
        flags=re.I,
    )
    html = re.sub(r'<link[^>]*jquery\.timepicker\.min\.css[^>]*>', "", html, flags=re.I)
    return html


def fix_framer_common(html: str) -> str:
    html = re.sub(
        r'<script[^>]*events\.framer\.com[^>]*></script>',
        "",
        html,
        flags=re.I,
    )
    html = re.sub(
        r'<script[^>]*googletagmanager\.com[^>]*></script>',
        "",
        html,
        flags=re.I,
    )
    html = re.sub(r'<div id="__framer-editorbar-container"[^>]*>[\s\S]*?</div>\s*</body>', "</body>", html)
    html = re.sub(r'<iframe id="__framer-editorbar"[^>]*></iframe>', "", html)
    html = re.sub(r'<div id="__framer-badge-container"[^>]*>[\s\S]*?</div>', "", html)
    return inject_head(html, FRAMER_HIDE, "framer-hide-vendor")


def fix_framer_imgs(html: str, pool: list[str]) -> str:
    idx = 0

    def next_img() -> str:
        nonlocal idx
        path = p(pool[idx % len(pool)])
        idx += 1
        return path

    def src_repl(_m: re.Match) -> str:
        return f'src="{next_img()}"'

    def url_repl(_m: re.Match) -> str:
        return f"url('{next_img()}')"

    def url_quot_repl(_m: re.Match) -> str:
        return f'url(&quot;{next_img()}&quot;)'

    pat = r"(?:https://|assets/)?framerusercontent\.com/images/[^\"')&]+\.(?:jpg|jpeg|png|webp)[^\"')&]*"
    html = re.sub(rf'src="({pat})"', src_repl, html, flags=re.I)
    html = re.sub(rf"url\((['\"]?)({pat})\1\)", url_repl, html, flags=re.I)
    html = re.sub(rf"url\(&quot;({pat})&quot;\)", url_quot_repl, html, flags=re.I)
    return html


def fix_wanderway(html: str) -> str:
    html = html.replace(
        "https://framerusercontent.com/sites/2Z0jOxojvxfwlf2wJNCM9J/",
        "assets/framerusercontent.com/sites/2Z0jOxojvxfwlf2wJNCM9J/",
    )
    html = html.replace(
        "https://framerusercontent.com/images/",
        "assets/framerusercontent.com/images/",
    )
    html = fix_framer_common(html)
    return fix_framer_imgs(html, [
        "01_hero_hero_thien_cam_beach_sunrise.png",
        "11_hero_wide_beach_sunrise_boats.png",
        "12_destination_coastal_road_mountain_sea.png",
        "54_lifestyle_friends_beach_walk_sunset.png",
        "10_experience_experience_ke_go_boat_tour.png",
    ])


def fix_luxestay(html: str) -> str:
    html = html.replace(
        "https://framerusercontent.com/sites/ecMzCdLOtbOd2HnKd7I0g/",
        "assets/framerusercontent.com/sites/ecMzCdLOtbOd2HnKd7I0g/",
    )
    html = html.replace(
        "https://framerusercontent.com/images/",
        "assets/framerusercontent.com/images/",
    )
    html = re.sub(r'href="([^"]+)\.mjs"', r'href="\1.mjs.js"', html)
    html = re.sub(r'src="([^"]+)\.mjs"', r'src="\1.mjs.js"', html)
    html = fix_framer_common(html)
    return fix_framer_imgs(html, LUXESTAY_IMG_POOL)


def fix_mountain(html: str) -> str:
    html = html.replace(
        "https://framerusercontent.com/sites/6EVz2XUDXvSpbx3lSth7Pk/",
        "assets/framerusercontent.com/sites/6EVz2XUDXvSpbx3lSth7Pk/",
    )
    html = html.replace(
        "https://framerusercontent.com/images/",
        "assets/framerusercontent.com/images/",
    )
    html = re.sub(r"<a[^>]*>.*?BUY THIS TEMPLATE.*?</a>", "", html, flags=re.I | re.S)
    html = fix_framer_common(html)
    return fix_framer_imgs(html, MOUNTAIN_IMG_POOL)


def _apply_vi_list(html: str, pairs: list[tuple[str, str]]) -> str:
    for old, new in pairs:
        html = html.replace(old, new)
    return html


def _moonlit_is_regex(pat: str) -> bool:
    return pat.startswith("(") or "\\" in pat or "(?:" in pat or pat.endswith("+")


def fix_moonlit(html: str) -> str:
    html = fix_crawl_artifacts(html)
    for old, new in MOONLIT_VI:
        if _moonlit_is_regex(old):
            html = re.sub(old, new, html)
        else:
            html = html.replace(old, new)
    imgs = [
        "08_hospitality_hospitality_beachfront_resort.png",
        "17_hospitality_modern_beach_hotel_exterior.png",
        "09_hospitality_hospitality_sea_view_room.png",
        "29_hospitality_luxury_sea_view_room.png",
        "45_hospitality_luxury_seaside_hotel_room.png",
        "48_hospitality_beach_resort_golden_hour.png",
    ]
    idx = 0

    def moon_img(m):
        nonlocal idx
        if idx >= len(imgs):
            return m.group(0)
        path = p(imgs[idx])
        idx += 1
        return f'src="{path}"'

    html = re.sub(
        r'src="assets/moonlit-react\.netlify\.app/assets/images/[^"]+\.(?:webp|jpg|jpeg|png)"',
        moon_img,
        html,
    )
    html = re.sub(r'<div class="gdpr-cookie-banner">[\s\S]*?</div>', "", html)
    html = re.sub(r"Cookies enable you to use shopping carts[\s\S]{0,400}?web searches\.", "", html)
    html = inject_head(html, MOONLIT_ICON_FALLBACK, "moonlit-icon-fallback")
    return html


def fix_hotale_uploads(html: str) -> str:
    for old, new in HOTALE_UPLOAD_MAP.items():
        html = html.replace(old, new)
        html = html.replace(f"assets/max-themes.net/demos/hotale/hotale/resort/{old}", new)
    return html


def fix_asatha_assets(html: str) -> str:
    idx = 0

    def img_repl(m: re.Match) -> str:
        nonlocal idx
        src = m.group(1)
        if "logo" in src.lower() or src.endswith(".svg"):
            return m.group(0)
        path = p(ASATHA_IMG_POOL[idx % len(ASATHA_IMG_POOL)])
        idx += 1
        return f'src="{path}"'

    html = re.sub(
        r'src="(assets/cdn\.prod\.website-files\.com/[^"]+\.(?:webp|jpg|jpeg|png))"',
        img_repl,
        html,
    )
    html = re.sub(r'\s+srcset="assets/cdn\.prod\.website-files\.com/[^"]*"', "", html)
    if "asatha-hide-vendor" not in html and "copyright-flowcub" in html:
        html = html.replace("</head>", ASATHA_HIDE + "</head>", 1)
    return html


def _travol_cycle(pool: list[str], pattern: str, html: str, attr: str = "src") -> str:
    idx = 0

    def repl(_m: re.Match) -> str:
        nonlocal idx
        path = p(pool[idx % len(pool)])
        idx += 1
        return f'{attr}="{path}"'

    return re.sub(pattern, repl, html)


def fix_travol_imgs(html: str) -> str:
    html = _travol_cycle(
        TRAVOL_DEST_IMGS,
        r'src="assets/duruthemes\.com/demo/html/travol/multipage-slider/img/destination/[^"]+\.jpg"',
        html,
    )
    html = _travol_cycle(
        TRAVOL_GALLERY_IMGS,
        r'src="assets/duruthemes\.com/demo/html/travol/multipage-slider/img/slider/[^"]+"',
        html,
    )
    html = _travol_cycle(
        TRAVOL_GALLERY_IMGS,
        r'href="assets/duruthemes\.com/demo/html/travol/multipage-slider/img/slider/[^"]+"',
        html,
        "href",
    )
    html = _travol_cycle(
        TRAVOL_BLOG_IMGS,
        r'src="assets/duruthemes\.com/demo/html/travol/multipage-slider/img/blog/[^"]+"',
        html,
    )
    html = _travol_cycle(
        TRAVOL_TEAM_IMGS,
        r'src="assets/duruthemes\.com/demo/html/travol/multipage-slider/img/team/0[123]\.jpg"',
        html,
    )
    html = _travol_cycle(
        TRAVOL_AVATAR_IMGS,
        r'src="assets/duruthemes\.com/demo/html/travol/multipage-slider/img/team/0[456]\.png"',
        html,
    )
    html = html.replace(
        'src="assets/duruthemes.com/demo/html/travol/multipage-slider/img/logo-light.png"',
        f'src="{p("01_hero_hero_thien_cam_beach_sunrise.png")}"',
    )
    if "travol-hide-clients" not in html and "img/clients/" in html:
        html = html.replace("</head>", TRAVOL_HIDE_CLIENTS + "</head>", 1)
    return html


def strip_vendor(html: str) -> str:
    for a, b in VENDOR_STRIP:
        html = html.replace(a, b)
    html = re.sub(
        r'href="https?://[^"]*(?:webflow\.com|flowcub|colorlib|duruthemes|max-themes|framer\.com)[^"]*"',
        'href="#"',
        html,
        flags=re.I,
    )
    return html


def process_html(fp: Path, html: str) -> str:
    slug = fp.relative_to(ROOT).parts[0]
    html = fix_crawl_artifacts(html)
    html = inject_head(html, GLOBAL_HIDE, "showcase-cleanup")
    html = strip_vendor(html)
    if slug == "seaside-webflow":
        html = fix_seaside_imgs(html)
    elif slug == "colorlib-deluxe":
        html = fix_colorlib(html)
    elif slug == "moonlit-react":
        html = fix_moonlit(html)
    elif slug in ("wanderway-framer", "luxestay-framer", "mountain-lodge-framer"):
        if slug == "wanderway-framer":
            html = fix_wanderway(html)
            html = _apply_vi_list(html, FRAMER_VI)
        elif slug == "luxestay-framer":
            html = fix_luxestay(html)
            html = _apply_vi_list(html, FRAMER_VI)
            html = _apply_vi_list(html, LUXESTAY_VI)
            html = html.replace("contact@LuxeStay Ha Tinh.demo", "contact@luxestay.demo")
        else:
            html = fix_mountain(html)
            html = _apply_vi_list(html, FRAMER_VI)
            html = _apply_vi_list(html, MOUNTAIN_VI)
    elif slug == "hotale-resort":
        html = fix_hotale_uploads(html)
    elif slug == "asatha-luxury-webflow":
        html = fix_asatha_assets(html)
    elif slug == "travol-duruthemes":
        html = fix_travol_imgs(html)
    return html


def symlink_luxestay_mjs():
    base = ROOT / "luxestay-framer" / "assets" / "framerusercontent.com" / "sites" / "ecMzCdLOtbOd2HnKd7I0g"
    if not base.exists():
        return
    for src in base.glob("*.mjs.js"):
        dst = src.with_suffix("")  # remove .js from .mjs.js -> .mjs
        if dst.suffix == ".mjs" and not dst.exists():
            try:
                shutil.copy2(src, dst)
            except OSError:
                pass


def main():
    count = 0
    for slug in ROOT.iterdir():
        if not slug.is_dir() or slug.name in ("assets", "docs", "tools", "webflow-bali-travel"):
            continue
        for fp in slug.rglob("*.html"):
            html = fp.read_text(encoding="utf-8", errors="ignore")
            new = process_html(fp, html)
            if new != html:
                fp.write_text(new, encoding="utf-8")
                count += 1
    symlink_luxestay_mjs()
    print(f"fix_showcase: updated {count} html files")
    print("luxestay mjs symlinks created")


if __name__ == "__main__":
    main()
