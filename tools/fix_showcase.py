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
a[href*="framer.market"],a[href*="framer.com/marketplace"],a[href*="lemonsqueezy.com"],
.framer-badge,.__framer-badge,#__framer-badge-container,[class*="buy-template"],[data-framer-component-type="Badge"],
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

MOONLIT_ICON_FALLBACK = """<style id="moonlit-icon-fallback">
[class^="flaticon-"]:before,[class*=" flaticon-"]:before{font-family:inherit!important;font-style:normal}
.flaticon-phone-flip:before{content:"\\260E"}
.flaticon-envelope:before{content:"\\2709"}
.flaticon-marker:before{content:"\\25CF"}
.flaticon-calendar:before{content:""}
.flaticon-user:before{content:"\\25CF"}
.flaticon-people:before{content:"\\25CF\\25CF"}
.flaticon-construction:before{content:""}
.flaticon-play:before{content:"\\25B6"}
.flaticon-star:before,.flaticon-star-sharp-half-stroke:before{content:"\\2605";color:#e9a225}
.flaticon-check-circle:before{content:"\\2713"}
.navigation__menu--item.has-arrow:before,.navigation__menu--item.has-arrow:after,
.navigation__menu--item ul.submenu li.has-arrow:before,.navigation__menu--item .sub__style li.has-arrow:before,
.navigation__menu--item.has-arrow>a:before,.navigation__menu--item.has-arrow>a:after,
.has-child.has-arrow>a:before,.has-child.has-arrow>a:after,
.navigation__menu--item.has-child>a:before,.navigation__menu--item.has-child>a:after,
.slide__menu__item .toggle,
.advance__search i[class*="flaticon-"],.query__input i,.query__input:before,.query__input:after{content:""!important;display:none!important;margin-left:0!important}
</style>"""

MOONLIT_LAYOUT_FIX = """<style id="moonlit-layout-fix">
html,body,#root{max-width:100%;overflow-x:hidden}
.banner__area .banner__slider,.banner__area .swiper-wrapper{width:100%!important;overflow:hidden!important;transform:none!important}
.banner__area .banner__slider .swiper-slide{display:none!important;width:100%!important;margin-right:0!important}
.banner__area .banner__slider .swiper-slide-active,.banner__area .banner__slider .swiper-slide:first-child{display:block!important}
.banner__area .banner__slider__image img{width:100%!important;height:100%!important;object-fit:cover!important}
.banner__area .banner__slide__content,.banner__area .banner__slide__content *{opacity:1!important;visibility:visible!important}
.banner__area .banner__slide__content{transform:none!important}
.banner__area .banner__slide__content h1{max-width:1000px;margin-left:auto;margin-right:auto;line-height:1.05}
.offcanvas:not(.show),.offcanvas-start:not(.show){visibility:hidden!important;transform:translateX(-100%)!important}
.header__top .social__links,.header__top .location{display:flex;flex-wrap:wrap;gap:18px}
.header__top .link__item,.navigation__menu--item__link,.main__right .theme-btn{white-space:nowrap}
@media(min-width:992px){
.main__header__wrapper{display:grid!important;grid-template-columns:minmax(0,1fr) auto auto;align-items:center;column-gap:clamp(20px,3vw,42px)}
.main__nav{min-width:0}
.main__logo{justify-self:center}
.navigation__menu>ul.list-unstyled{display:flex!important;align-items:center;flex-wrap:nowrap;gap:clamp(18px,1.8vw,30px);margin:0}
.navigation__menu--item{flex:0 0 auto}
.navigation__menu--item__link{font-size:17px!important}
.main__right{display:flex!important;align-items:center;gap:16px;flex-wrap:nowrap}
.main__right .theme-btn{min-width:0;padding-inline:22px}
.banner__area .banner__slide__content h1{font-size:clamp(68px,5.8vw,96px)!important}
}
</style>"""

COLORLIB_LAYOUT_FIX = """<style id="colorlib-layout-fix">
html,body{max-width:100%;overflow-x:hidden}
/* ftco-animate starts at opacity:0/visibility:hidden - needs JS to animate in */
.ftco-animate{opacity:1!important;visibility:visible!important}
/* Owl Carousel JS re-runs on pre-initialized HTML (double-init bug).
   The LEAVING slide (owl-animated-out) holds all real content but gets display:none.
   The ENTERING slide (owl-animated-in active) is empty.
   Fix: kill animations, show animated-out item, hide animated-in. */
.home-slider *{animation:none!important;-webkit-animation:none!important}
.home-slider{position:relative!important;height:900px!important;overflow:hidden!important}
.home-slider .owl-item{display:none!important}
/* Show the outer "leaving" slide which contains the real inner carousel.
   Owl JS sets left:1021px to push it off-screen — must override. */
.home-slider .owl-item.active,.home-slider .owl-item.owl-animated-out{display:block!important;opacity:1!important;width:100%!important;float:none!important;left:0!important;top:0!important;position:absolute!important}
/* Inside the leaving slide, show the inner carousel's active item */
.home-slider .owl-item.owl-animated-out .owl-item.active{display:block!important;opacity:1!important;width:100%!important;position:absolute!important}
/* Stage and outer layout */
.home-slider .owl-stage-outer{overflow:hidden!important;height:900px!important;max-width:100vw!important}
.home-slider .owl-stage{transform:none!important;width:100%!important;height:auto!important}
/* Slider item */
.home-slider .slider-item{height:900px;width:100%;display:block}
.home-slider .owl-animated-out .slider-item{opacity:1!important}
.home-slider .slider-item .overlay{background:linear-gradient(90deg,rgba(0,0,0,.4),rgba(0,0,0,.2))!important}
.home-slider .slider-text h1{max-width:1120px;margin-left:auto;margin-right:auto;line-height:1.05}
.popup-vimeo .icon-play:before{content:"\\25B6";font-family:Arial,sans-serif!important;font-size:30px;color:#fff;margin-left:4px}
.ftco-social .icon-twitter:before{content:"X";font-family:Arial,sans-serif!important;font-weight:700}
.ftco-social .icon-facebook:before{content:"f";font-family:Arial,sans-serif!important;font-weight:700}
.ftco-social .icon-google-plus:before{content:"G";font-family:Arial,sans-serif!important;font-weight:700}
.ftco-social .icon-instagram:before{content:"IG";font-family:Arial,sans-serif!important;font-size:12px;font-weight:700}
.ion-ios-arrow-down:before{content:"\\25BE";font-family:Arial,sans-serif!important}
.room .icon-instagram:before,.instagram .icon-instagram:before{content:"IG";font-family:Arial,sans-serif!important;font-size:13px;font-weight:700}
</style>"""

HOTALE_POLISH = """<style id="hotale-polish">
html,body{max-width:100%;overflow-x:hidden}
.hotale-body-wrapper{background:#f7f4ef}
.hotale-body-wrapper.hotale-with-frame{margin:0!important}
.hotale-body-wrapper .gdlr-core-pbf-wrapper:first-child{border-radius:0!important;min-height:760px!important;padding-top:220px!important}
.hotale-body-wrapper .gdlr-core-pbf-wrapper:first-child .gdlr-core-pbf-background-wrap{border-radius:0!important}
.hotale-header-wrap .hotale-header-container{max-width:1320px}
.hotale-header-wrap .hotale-header-container-inner{display:flex;align-items:center;gap:28px}
.hotale-header-wrap .hotale-logo{flex:0 0 170px;padding-left:0!important;padding-right:0!important}
.hotale-header-wrap .hotale-logo-inner span{font-size:19px!important}
.hotale-header-wrap .hotale-navigation{flex:1 1 auto;display:flex!important;align-items:center;justify-content:space-between;min-width:0;padding-left:0!important;padding-right:0!important}
.hotale-header-wrap .hotale-main-menu{flex:1 1 auto;min-width:0}
.hotale-header-wrap .sf-menu{display:flex!important;align-items:center;justify-content:center;flex-wrap:nowrap;gap:clamp(12px,1.2vw,20px);margin:0}
.hotale-header-wrap .sf-menu>li{float:none!important}
.hotale-header-wrap .sf-menu>li>a{padding:0!important;white-space:nowrap;font-size:14px!important;letter-spacing:.1em}
.hotale-main-menu-right-wrap{display:flex!important;align-items:center;gap:14px;flex:0 0 auto;white-space:nowrap;margin:0!important}
.tourmaster-currency-switcher,.tourmaster-room-navigation-checkout-wrap{float:none!important}
.tourmaster-room-navigation-checkout-button{white-space:nowrap}
body.home .title-rotate .gdlr-core-title-item-title{font-family:Georgia,'Times New Roman',serif!important;font-size:clamp(64px,5.2vw,90px)!important;line-height:1.05!important;letter-spacing:0!important;max-width:980px;margin-left:auto!important;margin-right:auto!important;text-shadow:0 10px 35px rgba(0,0,0,.35)}
body:not(.home) .title-rotate .gdlr-core-title-item-title{font-family:Georgia,'Times New Roman',serif!important;font-size:clamp(48px,4.2vw,72px)!important;line-height:1.08!important;letter-spacing:0!important;max-width:760px;margin-left:auto!important;margin-right:auto!important;text-shadow:0 10px 35px rgba(0,0,0,.35)}
body:not(.home) .hotale-body-wrapper .gdlr-core-pbf-wrapper:first-child{min-height:520px!important;padding-top:190px!important;padding-bottom:40px!important}
.gdlr-core-text-box-item-content p{line-height:1.55}
.tourmaster-room-search-wrap{box-shadow:0 22px 60px rgba(31,23,12,.18);border-radius:0!important;overflow:hidden}
.tourmaster-room-search-wrap .tourmaster-room-search-field{min-height:138px}
.tourmaster-room-search-submit{background:#8d6f3b!important;color:#fff!important;border-color:#8d6f3b!important}
.tourmaster-room-search-submit:hover{background:#755c31!important;border-color:#755c31!important}
.tourmaster-head{letter-spacing:.08em}
i.icon-phone:before{content:"\\260E";font-family:Arial,sans-serif!important}
i.icon-envelope:before{content:"\\2709";font-family:Arial,sans-serif!important}
i.icon_lock_alt:before{content:"\\25CB";font-family:Arial,sans-serif!important}
i.icon_close:before{content:"\\2715";font-family:Arial,sans-serif!important}
i.icon_plus:before{content:"\\002B";font-family:Arial,sans-serif!important}
i.icon_minus-06:before{content:"\\2212";font-family:Arial,sans-serif!important}
i.icon-arrow-right:before{content:"\\2192";font-family:Arial,sans-serif!important}
i.icon-arrow-left:before{content:"\\2190";font-family:Arial,sans-serif!important}
i.fa-sort-down:before{content:"\\25BE";font-family:Arial,sans-serif!important}
i.fa-facebook:before{content:"f";font-family:Arial,sans-serif!important;font-weight:700}
i.fa-instagram:before{content:"IG";font-family:Arial,sans-serif!important;font-size:.72em;font-weight:700}
i.fa-twitter:before{content:"X";font-family:Arial,sans-serif!important;font-weight:700}
i.fa-pinterest-p:before{content:"P";font-family:Arial,sans-serif!important;font-weight:700}
i.fa5-tiktok:before{content:"TT";font-family:Arial,sans-serif!important;font-size:.72em;font-weight:700}
.gdlr-icon-double-bed2:before{content:"\\1F6CF";font-family:"Segoe UI Symbol","Segoe UI Emoji",sans-serif!important}
.gdlr-icon-group:before{content:"\\1F465";font-family:"Segoe UI Symbol","Segoe UI Emoji",sans-serif!important}
.gdlr-icon-clock:before{content:"\\23F1";font-family:"Segoe UI Symbol","Segoe UI Emoji",sans-serif!important}
.tourmaster-room-content-wrap .tourmaster-info i{display:inline-block!important;width:18px!important;margin-right:7px!important;color:#8d6f3b!important;font-style:normal!important}
.tourmaster-room-content-wrap .tourmaster-info i:before{font-size:14px!important;line-height:1!important}
.gdlr-core-icon-item .gdlr-core-icon-item-icon{
  display:inline-flex!important;align-items:center;justify-content:center;
  width:72px!important;height:72px!important;min-width:72px!important;min-height:72px!important;
  border-radius:50%;background:rgba(255,255,255,.88);box-shadow:0 18px 45px rgba(0,0,0,.16);
  color:#8d6f3b!important;font-size:34px!important;line-height:1!important;
}
.gdlr-core-icon-item-icon:before{font-family:"Segoe UI Symbol","Segoe UI Emoji",sans-serif!important;font-style:normal!important}
.gdlr-icon-safe-box1:before{content:"\\1F512"}
.gdlr-icon-swimming-pool1:before{content:"\\1F3CA"}
.gdlr-icon-massage:before{content:"\\1F486"}
.gdlr-icon-weights:before{content:"\\1F3CB"}
.gdlr-icon-wifi-signal:before{content:"\\1F4F6"}
.gdlr-icon-breakfast:before{content:"\\2615"}
.gdlr-icon-workspace:before{content:"\\2328"}
.gdlr-core-image-item-wrap img[title="Group 40"]{
  width:72px!important;height:72px!important;object-fit:contain!important;padding:16px;border-radius:50%;
  background:rgba(255,255,255,.88);box-shadow:0 18px 45px rgba(0,0,0,.16);
}
#gdlr-core-wrapper-4{position:relative!important;padding-top:74px!important;padding-bottom:150px!important}
#gdlr-core-wrapper-4:before{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(255,248,235,.9),rgba(255,255,255,.58) 42%,rgba(255,255,255,.2));z-index:0;pointer-events:none}
#gdlr-core-wrapper-4>.gdlr-core-pbf-background-wrap,#gdlr-core-wrapper-4>.gdlr-core-pbf-wrapper-content{position:relative;z-index:1}
#gdlr-core-wrapper-4 .gdlr-core-title-item-title{color:#171717!important;text-shadow:0 1px 18px rgba(255,255,255,.45)}
#gdlr-core-wrapper-4 .gdlr-core-text-box-item-content{color:#4d5560!important}
#gdlr-core-wrapper-4 .gdlr-core-column-12 .gdlr-core-title-item-title{font-family:Arial,Helvetica,sans-serif!important;font-size:18px!important;font-weight:700!important;line-height:1.35!important;text-shadow:0 1px 16px rgba(255,255,255,.7)}
@media(max-width:1100px){
.hotale-header-wrap .hotale-header-container-inner{gap:18px}
.hotale-header-wrap .sf-menu{gap:14px}
.hotale-header-wrap .sf-menu>li>a{font-size:13px!important}
.hotale-main-menu-right-wrap{gap:12px}
}
@media(max-width:900px){.title-rotate .gdlr-core-title-item-title{font-size:42px!important}.hotale-body-wrapper .gdlr-core-pbf-wrapper:first-child{padding-top:170px!important}.hotale-header-wrap .hotale-header-container-inner{display:block}.hotale-header-wrap .hotale-navigation{display:block!important}}
.tourmaster-room-date-selection .tourmaster-tail:after{content:"\\25BE"!important;font-family:Arial,sans-serif!important}
</style>"""

MOUNTAIN_POLISH = """<style id="mountain-polish">
/* Reveal Framer scroll-triggered sections frozen at opacity:0 in offline snapshot */
#main [style*="opacity: 0"]{opacity:1!important;transform:none!important}
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
COLORLIB_IMG["images/image_8.jpg"] = f"{IMG}/48_hospitality_beach_resort_golden_hour.png"
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
    ("Deluxe Hotel Ha Tinh, she had a last view back on the skyline of her hometown Bookmarksgrove, the headline of Alphabet Village and the subline of her own road, the Line Lane. Pityful a rethoric question ran over her cheek, then she continued her way.", "KhÃ´ng gian lÆ°u trÃº Ä‘Æ°á»£c sáº¯p xáº¿p gá»n gÃ ng, cÃ³ khu áº©m thá»±c, dá»‹ch vá»¥ há»— trá»£ vÃ  cÃ¡c háº¡ng phÃ²ng phÃ¹ há»£p cho chuyáº¿n nghá»‰ táº¡i HÃ  TÄ©nh."),
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

HOTALE_VI = [
    ("About Us 2", "Giới thiệu thêm"),
    ("About Us 3", "Không gian nghỉ dưỡng"),
    ("Hotale – Hotel HTML Template", "Thien Cam Resort — Demo lưu trú Hà Tĩnh"),
    ('lang="en-US"', 'lang="vi"'),
    (">Home<", ">Trang chủ<"),
    (">Pages<", ">Trang<"),
    (">Reservation<", ">Đặt phòng<"),
    (">Blog<", ">Tin tức<"),
    (">Our Team<", ">Đội ngũ<"),
    (">Hotel Review<", ">Đánh giá<"),
    (">FAQ<", ">Câu hỏi thường gặp<"),
    (">Price Table<", ">Bảng giá<"),
    (">Maintenance<", ">Bảo trì<"),
    (">Coming Soon<", ">Sắp ra mắt<"),
    (">404 Page<", ">Trang lỗi<"),
    (">Single Posts<", ">Bài viết chi tiết<"),
    (">Blog Columns<", ">Bài viết dạng cột<"),
    (">Blog Full<", ">Bài viết toàn trang<"),
    (">Blog Grid<", ">Bài viết dạng lưới<"),
    (">Rooms<", ">Phòng<"),
    (">Contact<", ">Liên hệ<"),
    (">About Us<", ">Giới thiệu<"),
    (">About<", ">Giới thiệu<"),
    (">Gallery<", ">Thư viện<"),
    (">Room Grid Style 1<", ">Danh sách phòng<"),
    (">Room Grid Style 2<", ">Phòng view biển<"),
    (">Room Grid Style 3<", ">Suite gia đình<"),
    (">Room Grid Style 4<", ">Villa nghỉ dưỡng<"),
    (">Room Modern Style<", ">Phòng hiện đại<"),
    (">Room Side Thumbnail<", ">Chi tiết phòng<"),
    (">Book Now<", ">Đặt phòng<"),
    ("data-label=\"Book Now\"", "data-label=\"Đặt phòng\""),
    ("data-checkout-label=\"Check Out\"", "data-checkout-label=\"Trả phòng\""),
    ("<span>USD</span>", "<span>VND</span>"),
    (">Room</div>", ">Phòng</div>"),
    ("Book Now", "Đặt phòng"),
    ("Search Room", "Tìm phòng"),
    ("SEARCH ROOM", "TÌM PHÒNG"),
    ("Reservation", "Đặt phòng"),
    ("Pages", "Trang"),
    ("Home", "Trang chủ"),
    ("Blog", "Tin tức"),
    ("Our Team", "Đội ngũ"),
    ("Hotel Review", "Đánh giá"),
    ("Price Table", "Bảng giá"),
    ("Maintenance", "Bảo trì"),
    ("Coming Soon", "Sắp ra mắt"),
    ("Single Posts", "Bài viết chi tiết"),
    ("Login", "Đăng nhập"),
    ("Sign In!", "Đăng nhập"),
    ("Forgot Password?", "Quên mật khẩu?"),
    ("Create an Account", "Tạo tài khoản"),
    ("Already a Member?", "Đã có tài khoản?"),
    ("Username*", "Tên đăng nhập*"),
    ("First Name*", "Tên*"),
    ("Last Name*", "Họ*"),
    ("Birth Date*", "Ngày sinh*"),
    ("Country*", "Quốc gia*"),
    ("Password*", "Mật khẩu*"),
    ("Confirm Password*", "Xác nhận mật khẩu*"),
    ("Phone*", "Điện thoại*"),
    ("Email*", "Email*"),
    ("Date", "Ngày"),
    ("Month", "Tháng"),
    ("Year", "Năm"),
    ("United States of America (USA)", "Việt Nam"),
    ("Creating an account means you're okay with our Terms of Service and Privacy Statement.", "Tạo tài khoản demo để xem giao diện đặt phòng và dịch vụ."),
    ("SIGN UP", "ĐĂNG KÝ"),
    ("Người lớns", "người lớn"),
    ("Jul 28, 2022", "14/06/2026"),
    ("Jul 29, 2022", "15/06/2026"),
    ("Some Useful Travel Tips", "Gợi ý cho kỳ nghỉ Thiên Cầm"),
    ("Travel Planning", "Lên lịch trình"),
    ("My 6 Biggest Travel Surprises", "Những trải nghiệm đáng nhớ ở Hà Tĩnh"),
    ("Why I Quit My Job To Be A Less Occasional Traveller In 2019", "Khi kỳ nghỉ ngắn trở thành thói quen sống chậm"),
    ("Far far away, behind the word mountains", "Bên bờ biển Thiên Cầm"),
    ("there live the blind texts", "có những trải nghiệm nghỉ dưỡng yên tĩnh"),
    ("Bookmarksgrove", "Thiên Cầm"),
    ("Vokalia and Consonantia", "Hà Tĩnh"),
    (
        "Our hotel is located in the heart of the New Forrest. A five stars lifestyle surrounded by the forest.",
        "Thiên Cầm Resort tọa lạc ven bờ biển Thiên Cầm, Cẩm Xuyên, Hà Tĩnh — không gian lưu trú hiện đại dành cho gia đình và kỳ nghỉ ngắn.",
    ),
]

MOONLIT_VI_EXTRA = [
    # Google Maps embed: thay Phuket → Hà Tĩnh
    (
        "maps?width=100%25&amp;height=600&amp;hl=en&amp;q=phuket+(My%20Business%20Họ tên)&amp;t=&amp;z=14&amp;ie=UTF8&amp;iwloc=B&amp;output=embed",
        "maps?width=100%25&amp;height=600&amp;hl=vi&amp;q=Thiên Cầm, Cẩm Xuyên, Hà Tĩnh&amp;t=&amp;z=13&amp;ie=UTF8&amp;iwloc=B&amp;output=embed",
    ),
    ("Luxury Hotel", "Khách sạn Hà Tĩnh"),
    ("Luxe Vista", "Villa hướng biển"),
    ("Ocean Breeze", "Phòng biển Thiên Cầm"),
    ("Rooms & Suites", "Phòng & suite"),
    (">Rooms<", ">Phòng<"),
    (">About<", ">Giới thiệu<"),
    (">About us<", ">Giới thiệu<"),
    (">Restaurant<", ">Nhà hàng<"),
    (">Contact<", ">Liên hệ<"),
    (">Contact Us<", ">Liên hệ<"),
    (">Book Now<", ">Xem phòng<"),
    ("Book Now", "Xem phòng"),
    ("Login To Moonlit", "Đăng nhập Moonlit"),
    ("Welcome to Career Compass, your ultimate destination for career advice, job search strategies, and professional development insights. Whether you're a recent graduate, seasoned professional, or someone considering a career change, our blog is your trusted guide to help you navigate the ever-evolving landscape of the job market.", "Moonlit chia sẻ kinh nghiệm lưu trú, gợi ý lịch trình và những lựa chọn nghỉ dưỡng phù hợp cho chuyến đi Hà Tĩnh."),
    ("Urban Oasis Living", "Nghỉ dưỡng ven biển"),
    ("Discover the Ultimate Mountain Getaway", "Trải nghiệm nghỉ dưỡng yên tĩnh tại Hà Tĩnh"),
    ("Our diverse range of activities is designed to offer something for everyone.", "Hoạt động nghỉ dưỡng được chọn lọc cho gia đình, cặp đôi và nhóm bạn."),
    ("A Night of Hope: Our Charity Gala Room.", "Không gian sự kiện ấm cúng bên biển Thiên Cầm."),
    ("Taste of Luxury: Food &amp; Wine Festival Sự kiện", "Đêm ẩm thực và hải sản Hà Tĩnh"),
    ("At our Fitness &amp; Yoga Dịch vụs, we are dedicated to helping you achieve your health and wellness goals. Our comprehensive program offers a variety of classes designed to suit all levels, from beginners to advanced practitioners.", "Moonlit chuẩn bị không gian linh hoạt cho tiệc tối, hội nghị nhỏ và các hoạt động thư giãn trong kỳ nghỉ."),
    ("Guest Dinner", "khách dự tiệc"),
    ("Dịch vụ Man", "nhân sự phục vụ"),
    ("Special Room", "không gian riêng"),
    ("Enter your email", "Nhập email"),
    ("Enter your password", "Nhập mật khẩu"),
    ("Forgot Mật khẩu?", "Quên mật khẩu?"),
    ("Continue with Google", "Tiếp tục với Google"),
    ("Continue with Facebook", "Tiếp tục với Facebook"),
    ("Don’t have an account?", "Chưa có tài khoản?"),
    ("Have an account?", "Đã có tài khoản?"),
    ("Candidate", "Nguyễn An"),
    ("Phone</span>", "Điện thoại</span>"),
    ("Address</span>", "Địa chỉ</span>"),
    ("Guest Dịch vụ", "Dịch vụ khách"),
    ("Hotel Dịch vụ", "Dịch vụ khách sạn"),
    ("Hotel Service", "Dịch vụ khách sạn"),
    ("Romantic Getaway", "Kỳ nghỉ lãng mạn"),
    ("Family Vacation", "Kỳ nghỉ gia đình"),
    ("Event Planning", "Tổ chức sự kiện"),
    ("Sự kiện Planning", "Tổ chức sự kiện"),
    ("Seasonal Promotions", "Ưu đãi theo mùa"),
    ("Conference Venues", "Không gian hội nghị"),
    ("Special Offers", "Ưu đãi riêng"),
    ("Real Guest Stories: Unforgettable Stays at Bokinn", "Câu chuyện lưu trú đáng nhớ tại Moonlit"),
    ("Real Guest Stories: Unforgettable Stays at Moonlit", "Câu chuyện lưu trú đáng nhớ tại Moonlit"),
    ("Tags", "Chủ đề"),
    ("Hotel Stay", "Lưu trú"),
    ("Travel Blog", "Du lịch Hà Tĩnh"),
    ("Guest Experience", "Trải nghiệm khách"),
    ("Hotel Guide", "Gợi ý lưu trú"),
    ("Hotel Review", "Đánh giá khách sạn"),
    ("Share", "Chia sẻ"),
    ("Leave a Comment", "Gửi bình luận"),
    ("Your Name", "Họ tên"),
    ("Your Email", "Email của bạn"),
    ("Your Comment", "Nội dung bình luận"),
    ("Your message", "Nội dung của bạn"),
    ("Submit Comment", "Gửi bình luận"),
    ("Comment", "Bình luận"),
    ("Reply", "Trả lời"),
    ("A week ago", "Một tuần trước"),
    ("Top 10 Reasons Guests Love Staying at Bokinn", "Lý do khách yêu thích Moonlit"),
    ("Search", "Tìm kiếm"),
    ("Latest Post", "Tin mới"),
    ("Adventure Stays", "Nghỉ dưỡng khám phá"),
    ("Wellness & Relaxation", "Thư giãn & chăm sóc"),
    ("Cultural Stays", "Trải nghiệm văn hóa"),
    ("Historic Hotels", "Lưu trú gần di tích"),
    ("Pet-Friendly Hotels", "Thân thiện thú cưng"),
    ("Extra Dịch vụs", "Dịch vụ thêm"),
    ("Room Clean", "Dọn phòng"),
    ("Airport transport", "Đưa đón"),
    ("Pet-Friendly", "Thân thiện thú cưng"),
    ("Total Price", "Tổng cộng"),
    ("Book Your Room", "Đặt phòng"),
    ("Similar Rooms", "Phòng tương tự"),
    ("Discover More", "Xem thêm"),
    ("Moonlit@gmail.com", "contact@moonlit.demo"),
    ("Ashiq", "Moonlit Team"),
    ("Jonathon Doe", "Nguyễn An"),
    ("Michael Roy", "Trần Minh"),
    ("10 Min Read", "5 phút đọc"),
    ("Moonlit Hotel là lựa chọn lưu trú tin cậy tại Hà Tĩnh.,", "Moonlit Hotel là lựa chọn lưu trú tin cậy tại Hà Tĩnh,"),
    ("Watch Now * Watch Now * Watch Full Video *", "Xem trải nghiệm * Xem video * Moonlit Hotel *"),
    # moonlit restaurant.html: English body paragraphs
    ("Whether you are in the mood for a leisurely breakfast, a business lunch, or a romantic dinner.", "Dù bạn muốn bữa sáng nhẹ nhàng, bữa trưa công việc hay tối lãng mạn — Moonlit sẵn sàng đáp ứng mọi khoảnh khắc."),
    ("From Farm to Fork: Enjoy Fresh, Seasonal Dishes at Moonlit", "Từ vườn đến bàn ăn: Thưởng thức món tươi theo mùa tại Moonlit"),
    ("Our rooms offer a harmonious blend of comfort and elegance, designed to provide an exceptional stay for every guest Each room features plush bedding.", "Phòng nghỉ kết hợp hài hòa giữa tiện nghi và sang trọng, thiết kế để mỗi lượt lưu trú đều đáng nhớ."),
    # moonlit service.html: English service descriptions
    ("At Moonlit we pride ourselves on delivering an exceptional experience.", "Tại Moonlit, chúng tôi tự hào mang đến trải nghiệm dịch vụ xuất sắc."),
    ("A 24-hour security service provides and surveillance, properties, or sensitive information around the clock.", "Dịch vụ an ninh 24/7 đảm bảo an toàn tuyệt đối cho khách và tài sản suốt ngày đêm."),
    ("Wi-Fi miễn phí has become an essential service in our increasingly connected world. It by people to access the internet", "Wi-Fi miễn phí tốc độ cao — kết nối liên tục trong mọi khu vực của khách sạn."),
    ("A fitness center is a vibrant and dynamic environment designed to promote health and Fitnee Center well-being.", "Phòng tập thể dục năng động, trang bị hiện đại để hỗ trợ sức khỏe và thể lực của khách."),
    ("Đưa đónation plays a crucial role in travel experiences for passengers. It various services, including taxis, ride-sharing", "Dịch vụ đưa đón sân bay và di chuyển nội thành — tiện lợi, đúng giờ và thoải mái."),
    ("A well-organized work desk is more than just a place to complete tasks; it's a hub of productivity and creativity.", "Bàn làm việc gọn gàng, đầy đủ ánh sáng — không gian lý tưởng cho công việc và sáng tạo."),
    ("A swimming pool is a refreshing oasis, offering a place to cool off, relax, and enjoy various water activities.", "Hồ bơi trong xanh — nơi thư giãn, giải nhiệt và tận hưởng các hoạt động dưới nước."),
    ("On-site security personnel and surveillance. from standard to luxury suites, Secure it is storage for valuables.", "Nhân viên an ninh thường trực và két an toàn — bảo vệ tài sản từ phòng tiêu chuẩn đến suite cao cấp."),
    ("The warm water cascaded down, enveloping a soothing as I stood in the shower. Each droplet danced on my skin, washing.", "Vòi sen mưa ấm áp bao phủ, mỗi giọt nước như xoa dịu mọi mệt mỏi — không gian tắm được chăm chút từng chi tiết."),
    # moonlit blog.html: English intro paragraphs
    ("Discover The blog where luxury, comfort, and adventure come together.", "Khám phá blog nơi sang trọng, tiện nghi và phiêu lưu hội tụ tại Hà Tĩnh."),
    ("Live Elegantly in Our Contemporary Suite for Apartment", "Sống thanh lịch trong Suite hiện đại của Moonlit"),
    (
        "In today's ever-evolving business landscape, staying ahead of the curve is essential for success. Whether you're a seasoned entrepreneur or just starting out, the key to thriving in this dynamic environment lies in adaptability and innovation.",
        "Moonlit chia sẻ những gợi ý du lịch, mẹo lưu trú và trải nghiệm đáng nhớ tại Hà Tĩnh để chuyến đi của bạn luôn trọn vẹn và thư thái.",
    ),
]

COLORLIB_VI_EXTRA = [
    (">About<", ">Giới thiệu<"),
    (">Contact<", ">Liên hệ<"),
    ("About Us", "Giới thiệu"),
    ("Contact Us", "Liên hệ"),
    ("Travel", "Du lịch"),
    ("Destination", "Điểm đến"),
    ("0 Children", "0 trẻ em"),
    ("1 Children", "1 trẻ em"),
    ("2 Children", "2 trẻ em"),
    ("3 Children", "3 trẻ em"),
    ("4 Children", "4 trẻ em"),
    ("5 Children", "5 trẻ em"),
    ("6 Children", "6 trẻ em"),
    (
        "Deluxe Hotel Ha Tinh, she had a last view back on the skyline of her hometown Thiên Cầm, the headline of Alphabet Village and the subline of her own road, the Line Lane. Pityful a rethoric question ran over her cheek, then she continued her way.",
        "Deluxe Hotel Ha Tinh mang đến không gian lưu trú tiện nghi gần biển Thiên Cầm, phù hợp cho kỳ nghỉ ngắn ngày, chuyến công tác và gia đình muốn khám phá Hà Tĩnh.",
    ),
    (
        "far from the countries Vokalia and Consonantia, there live the blind texts.",
        "với dịch vụ chu đáo, phòng nghỉ yên tĩnh và vị trí thuận tiện để khám phá Hà Tĩnh.",
    ),
    ("We Are Food Lover", "Ẩm Thực Hà Tĩnh"),
    (">Restaurants<", ">Ẩm thực<"),
    (">RESTAURANTS<", ">ẨM THỰC<"),
    ("Advanced Search", "Tìm kiếm nâng cao"),
    ("Star Rating", "Xếp hạng sao"),
]

FRAMER_VI_EXTRA = [
    ("Wanderway", "Wander Hà Tĩnh"),
    ("WanderWay", "Wander Hà Tĩnh"),
    ("WanderWay HÃ  TÄ©nh", "Wander Hà Tĩnh"),
    ("A glimpse into our world", "Một góc nghỉ dưỡng Hà Tĩnh"),
    ("Mountains and Valleys", "Hồ Kẻ Gỗ và rừng núi"),
    ("Living spaces", "Không gian lưu trú"),
    ("Living Spaces", "Không gian lưu trú"),
    ("Food and Drink", "Ẩm thực địa phương"),
    ("Restaurants", "Nhà hàng"),
    ("Discover New Horizons", "Khám phá Hà Tĩnh"),
    ("Start your adventure today and explore the world with Wander Hà Tĩnh!", "Bắt đầu hành trình khám phá biển, hồ và di tích Hà Tĩnh."),
    ("Start your adventure today and explore the world with Wander HÃ  TÄ©nh!", "Bắt đầu hành trình khám phá biển, hồ và di tích Hà Tĩnh."),
    ("Start your adventure today and explore the world with Wanderway!", "Bắt đầu hành trình khám phá biển, hồ và di tích Hà Tĩnh."),
    ("About Company", "Giới thiệu"),
    ("Discounts", "Ưu đãi"),
    ("Our News", "Tin mới"),
    ("Always Within Reach", "Luôn sẵn sàng hỗ trợ"),
    ("Wander Hà Tĩnh HQ, 1234 West End Avenue, Suite 7, Los Angeles", "Trung tâm hỗ trợ du lịch Hà Tĩnh, TP. Hà Tĩnh"),
    ("Wander HÃ  TÄ©nh HQ, 1234 West End Avenue, Suite 7, Los Angeles", "Trung tâm hỗ trợ du lịch Hà Tĩnh, TP. Hà Tĩnh"),
    ("(239) 555-0108", "0239 385 6789"),
    ("(406) 555-0120", "0239 368 1888"),
    ("Download Our App", "Thông tin đặt lịch"),
    ("Plan, book, and manage your trips on the go - download our app now!", "Liên hệ để được gợi ý lịch trình, đặt phòng và trải nghiệm phù hợp."),
    ("Plan, book, and manage your trips on the go – download our app now!", "Liên hệ để được gợi ý lịch trình, đặt phòng và trải nghiệm phù hợp."),
    ("Your Dream Island Adventure", "Hành trình biển Hà Tĩnh"),
    ("Escape to Paradise: Hot Island Tour You Can’t Miss!", "Khám phá Thiên Cầm và ven biển Hà Tĩnh"),
    ("Escape to Paradise: Hot Island Tours You Can’t Miss!", "Khám phá Thiên Cầm và ven biển Hà Tĩnh"),
    ("Escape To Paradise: Hot Island Tour You Can’t Miss!", "Khám phá Thiên Cầm và ven biển Hà Tĩnh"),
    ("Escape To Paradise: Hot Island Tours You Can’t Miss!", "Khám phá Thiên Cầm và ven biển Hà Tĩnh"),
    ("Your Next Tropical Adventure is Just a Click Away", "Hành trình biển xanh đang chờ bạn"),
    ("Price packages", "Bảng giá tour"),
    ("ALL PAGES", "TRANG"),
    ("All Pages", "Trang"),
    ("All Rights Reserved", "Đã đăng ký bản quyền"),
    ("Designed by ", ""),
    ("Designed by Fourtwelve", ""),
    ("Fourtwelve", ""),
    ("Unforgettable", "Đáng nhớ"),
    ("Explore", "Khám phá"),
    ("Travel", "Du lịch"),
    ("Tour", "Tour"),
    ("Services", "Dịch vụ"),
    ("Testimonials", "Đánh giá"),
    ("Contact Us", "Liên hệ"),
    ("About Us", "Giới thiệu"),
    ("Destination", "Điểm đến"),
    ("Remain abreast of the latest news, exclusive offers, exciting events, and beyond", "Nhận tin mới, ưu đãi và lịch trải nghiệm tại Hà Tĩnh."),
    ("GOOGLE FONTS", "FONT CHỮ"),
    ("typography", "kiểu chữ"),
    ("Google Fonts", "Google Fonts"),
    # wanderway heading fixes (EN fragments remaining after partial translation)
    ("Experiences from Start to Finish", "Hà Tĩnh — Trọn hành trình"),
    ("Dream tours", "Tour nổi bật"),
    ("Turning your travel desires into adventures", "Biến ước mơ du lịch thành hành trình thực"),
    # wanderway blog: foreign locations (Interlaken/Switzerland/Cappadocia/Turkey + Dubai→Cảng cá artifact)
    (
        "Paragliding in Interlaken, Switzerland offers views that stretch from snowcaps to lakes; "
        "skydiving over Cảng cá paints the desert in gold beneath your feet; "
        "and hot-air ballooning in Cappadocia, Turkey turns sunrise into pure magic.",
        "Chèo thuyền trên hồ Kẻ Gỗ giữa rừng xanh bạt ngàn; lướt sóng tại Thiên Cầm với bờ cát trắng trải dài; "
        "và leo núi Hương Tích ngắm toàn cảnh Hà Tĩnh từ trên cao — mỗi trải nghiệm là một kỷ niệm không thể quên.",
    ),
    # wanderway: mixed EN/VI artifacts từ partial word replacement
    ("One Happy Du lịcher at a Time!", "Mỗi hành trình là một kỷ niệm đáng nhớ!"),
    (
        "Khám phá thế giới with us: follow our social media for daily travel inspiration and updates!",
        "Theo dõi chúng tôi để cập nhật cảm hứng du lịch và ưu đãi mới nhất từ Hà Tĩnh!",
    ),
    ("Let Us Take You to Đáng nhớ điểm đến!", "Để chúng tôi đưa bạn đến những điểm đến đáng nhớ!"),
    # wanderway about-us: English body copy
    (
        "At Wander Hà Tĩnh, our journey with you starts from the moment you decide to explore the world. We believe that every trip is unique, and our travel planning process is designed to capture the essence of your ideal adventure. Whether it's customizing your accommodation, handling complex itineraries, we deliver seamless travel experiences made just for you.",
        "Tại Wander Hà Tĩnh, hành trình cùng bạn bắt đầu từ khoảnh khắc bạn quyết định khám phá vùng đất này. Chúng tôi tin rằng mỗi chuyến đi là độc nhất — từ chỗ ở đến lịch trình, mọi trải nghiệm đều được tuyển chọn để phù hợp với bạn nhất.",
    ),
    (
        "At Wander Hà Tĩnh, we believe that travel is more than just visiting new places—it's about creating unforgettable memories, experiencing diverse cultures, and exploring the world’s most breathtaking destinations.",
        "Tại Wander Hà Tĩnh, chúng tôi tin rằng du lịch không chỉ là đến nơi mới — đó là tạo ra ký ức đáng nhớ, trải nghiệm văn hóa địa phương và khám phá những điểm đến tuyệt vời nhất Hà Tĩnh.",
    ),
    ("Ready for a Getaway? Khám phá Our Hottest Du lịch Offers", "Sẵn sàng cho kỳ nghỉ? Khám phá những tour nổi bật tại Hà Tĩnh"),
    (
        "Stay connected with Wander Hà Tĩnh as we take you on a journey across the globe, sharing every thrilling adventure, breathtaking destination, and hidden gem through our social media channels.",
        "Theo dõi Wander Hà Tĩnh để cập nhật những trải nghiệm du lịch thú vị, điểm đến ẩn mình và ưu đãi mới nhất qua các kênh mạng xã hội của chúng tôi.",
    ),
    (
        "From sunrise hikes to sunset cruises, and from vibrant cityscapes to remote islands, we capture the essence of travel in real time.",
        "Từ chuyến đi bộ lúc bình minh đến du thuyền lúc hoàng hôn, từ khu phố sầm uất đến bờ biển hoang sơ — chúng tôi ghi lại cảm xúc du lịch trong từng khoảnh khắc.",
    ),
    ("20 Million tours conducted, each filled with unforgettable experiences and lasting memories.", "Hàng nghìn lượt khách đã khám phá Hà Tĩnh cùng chúng tôi, mang về những kỷ niệm không thể quên."),
    ("50+ expertly designed new travel routes tailored to explore the world’s most breathtaking destinations.", "50+ lộ trình được thiết kế riêng để khám phá những điểm đến đẹp nhất Hà Tĩnh và vùng lân cận."),
    ("98% of our travelers return home happy, satisfied, and eager to book their next adventure with us.", "98% du khách hài lòng và sẵn sàng quay lại cùng Wander Hà Tĩnh trong chuyến tiếp theo."),
    ("The Experts Who Turn Dreams into Journeys of a Lifetime", "Đội ngũ chuyên nghiệp biến ước mơ du lịch thành hành trình đáng nhớ"),
    # wanderway tours_cuba: Havana/Cuba-specific locations
    (
        "Step into a world of vivid color, music, and history as your journey begins in Havana — a city where every street tells a story. The first two days are devoted to discovering the essence of Hương Tích's capital: its colonial charm, lively rhythms, and the spirit of resilience that defines its people. From classic cars and cobblestone alleys to local artists and storytellers, Havana offers an inspiring introduction to the island's culture and educational heritage.",
        "Bắt đầu hành trình khám phá Hà Tĩnh với những con phố đầy màu sắc, âm nhạc dân ca và di tích lịch sử. Hai ngày đầu dành để cảm nhận nhịp sống của thành phố Hà Tĩnh — từ phố cổ, chợ truyền thống đến những nghệ nhân địa phương và câu chuyện về mảnh đất này.",
    ),
    (
        "Arrive at José Martí International Airport and transfer to a boutique hotel in Old Havana. Take time to relax before joining your fellow travelers for a welcome orientation and dinner featuring classic Hương Tíchn cuisine.",
        "Đến sân bay Vinh, di chuyển về Hà Tĩnh và nhận phòng khách sạn boutique. Thư giãn trước khi cùng đoàn tham dự buổi gặp mặt chào mừng với bữa tối đặc sản Hà Tĩnh.",
    ),
    ("Day 1–2: Arrival and Introduction to Havana", "Ngày 1–2: Đến Hà Tĩnh — Khám phá thành phố biển"),
    ("Evening music session at a local jazz bar", "Buổi tối thưởng thức dân ca ví dặm tại quán nhạc địa phương"),
    ("Dive deeper into Havana's artistic spirit.", "Khám phá sâu hơn tinh thần nghệ thuật và văn hóa Hà Tĩnh."),
    ("Viñales Valley", "Thung lũng Kẻ Gỗ"),
    ("Cienfuegos", "Cửa Nhượng"),
    ("Old Havana", "Phố cổ Hà Tĩnh"),
    ("Havana", "Hà Tĩnh thành phố"),
    # wanderway tours_spain: generic English intro paragraphs
    (
        "Join us for a journey that blends adventure, culture, and tranquility, crafted with care and passion for discovery. Wander Hà Tĩnh’s exclusive expedition invites you to experience the world’s timeless wonders in a way that’s both unique and unforgettable",
        "Cùng khởi đầu hành trình kết hợp phiêu lưu, văn hóa và sự yên bình — được thiết kế với tâm huyết và đam mê khám phá. Expedition đặc quyền của Wander Hà Tĩnh mời bạn trải nghiệm những điều kỳ diệu của vùng đất theo cách độc đáo và không thể quên",
    ),
    (
        "Step into an unforgettable adventure that blends history, culture, and natural beauty. This exclusive 14-day journey will immerse you in breathtaking landscapes, awe-inspiring monuments, and ancient traditions. Guided by local experts and staying in ",
        "Bước vào hành trình đáng nhớ kết hợp lịch sử, văn hóa và vẻ đẹp thiên nhiên. Chuyến đi 14 ngày độc quyền này sẽ đưa bạn đến những cảnh quan ngoạn mục, công trình ấn tượng và phong tục cổ xưa. Được dẫn dắt bởi chuyên gia địa phương và lưu trú tại ",
    ),
    # wanderway index.html: EN passion paragraph (curly apostrophe)
    (
        "Our passion for exploration fuels us to craft personalized experiences that dive deep into the heart of each destination. Let’s make your travel dreams a reality!",
        "Niềm đam mê khám phá thôi thúc chúng tôi tạo ra những trải nghiệm cá nhân hóa, đi sâu vào trái tim của mỗi điểm đến. Hãy để chúng tôi biến giấc mơ du lịch của bạn thành hiện thực!",
    ),
    # wanderway blog.html: EN intro
    (
        "We are passionate about curating exceptional travel experiences tailored to your unique interests and desires.",
        "Chúng tôi đam mê tuyển chọn những trải nghiệm du lịch xuất sắc, phù hợp với sở thích và mong muốn riêng của bạn.",
    ),
    # wanderway services.html
    ("Authentic encounters that connect you with culture and people.", "Những gặp gỡ chân thực kết nối bạn với văn hóa và con người địa phương."),
    # wanderway pricing.html: mixed EN/VI artifact
    ("Choose Your Path: From khách to Globetrotter", "Chọn hành trình của bạn: từ du khách đến nhà thám hiểm"),
    # wanderway our-team.html: USD price
    ("Discover the magic of Hà Tĩnh, with packages starting at $620.", "Khám phá vẻ đẹp Hà Tĩnh, với các gói tour từ 14.500.000đ."),
    # wanderway tours.html: mixed EN/VI
    (
        "Khám phá vẻ đẹp of Thiên Cầm, a land of golden coasts, vibrant culture, and timeless architectural wonders.",
        "Khám phá vẻ đẹp Thiên Cầm — bờ biển vàng, văn hóa sôi động và những kỳ quan kiến trúc vượt thời gian.",
    ),
    # wanderway destination.html
    ("Let each destination be the start of a new story.", "Để mỗi điểm đến là khởi đầu của một câu chuyện mới."),
    # wanderway testimonials (curly apostrophe in Wander Hà Tĩnh)
    # tours_cuba join intro
    (
        "Join us for a journey that celebrates rhythm, history, and discovery. Wander Hà Tĩnh’s educational expedition invites you to explore Hương Tích’s vibrant culture",
        "Cùng khởi đầu hành trình văn hóa và khám phá vùng đất Hà Tĩnh cùng Wander Hà Tĩnh",
    ),
]

MOUNTAIN_VI_EXTRA = [
    ("Mountain Lodge", "Ke Go Eco Lodge"),
    ("YOUR PERFECT GETAWAY", "RETREAT BÊN HỒ KẺ GỖ"),
    ("Escape to our enchanting mountain lake boutique hotel, where every moment is a masterpiece of natural beauty. Embrace serenity amidst breathtaking views of towering mountains and tranquil waters", "Không gian nghỉ dưỡng ven hồ Kẻ Gỗ với nhịp sống chậm, cảnh rừng yên tĩnh và những góc lưu trú gần thiên nhiên Hà Tĩnh."),
    ("Immerse yourself in the lavish embrace of sumptuously appointed chambers and an exquisitely crafted ambiance, where every detail whispers of refined luxury and timeless elegance.", "Phòng nghỉ sử dụng hình ảnh địa phương, chất liệu ấm và bố cục gọn để tạo cảm giác thư giãn sau một ngày khám phá hồ Kẻ Gỗ."),
    ("We offer a range of meticulously curated phòng to suit every discerning guest. Experience unparalleled luxury and comfort in our Deluxe Suites, boasting panoramic views of the serene surroundings and plush tiện ích for a rejuvenating stay. For those seeking a touch of opulence, our Executive Phòng provide an exquisite blend of sophistication and convenience, featuring elegant furnishings and personalized services. ", "Các hạng phòng được sắp xếp cho nhiều nhu cầu: nghỉ cuối tuần, đi cùng gia đình hoặc chuyến retreat nhỏ. Mỗi phòng ưu tiên ánh sáng tự nhiên, tầm nhìn xanh và tiện ích vừa đủ cho kỳ nghỉ ngắn. "),
    ("Unwind in style and comfort in our cozy yet chic Boutique Phòng, offering a peaceful retreat after a day of exploration. From complimentary high-speed Wi-Fi to indulgent room service, every aspect of your stay is tailored to exceed expectations and create unforgettable memories.", "Sau lịch trình tham quan, khách có thể nghỉ trong không gian yên tĩnh, dùng bữa nhẹ và chuẩn bị cho trải nghiệm chèo thuyền, đi rừng hoặc khám phá ẩm thực địa phương."),
    ("ABOUT", "GIỚI THIỆU"),
    ("ROOMS", "PHÒNG"),
    ("AREA", "KHU VỰC"),
    ("RESTAURANTS", "ẨM THỰC"),
    ("EVENTS", "SỰ KIỆN"),
    ("CONTACT", "LIÊN HỆ"),
    ("BOOK", "ĐẶT PHÒNG"),
    ("BUY THIS TEMPLATE", ""),
    ("Gallery", "Thư viện"),
    ("GIẤY PHÉP", "Thông tin mẫu"),
    ("GOOGLE FONTS", "FONT CHỮ"),
    ("Remain abreast of the latest news, exclusive offers, exciting events, and beyond", "Nhận tin mới, ưu đãi và lịch trải nghiệm tại Kẻ Gỗ."),
    ("+40 482 430 3205", "0239 385 6789"),
    ("20121", "Hà Tĩnh"),
    # area.html / rooms.html: Italian Alps và body copy còn tiếng Anh
    ("Surrender to the comfort of our peaceful retreat", "Đắm mình trong không gian yên tĩnh bên hồ Kẻ Gỗ"),
    ("Indulge in the Beauty of our Region", "Khám phá vẻ đẹp khu vực hồ Kẻ Gỗ"),
    (
        "Discover the allure of the wine traditions in the Italian Alps at our exclusive hotel, nestled amongst stunning mountain vistas. Enjoy an expertly chosen array of local wines from neighboring hamlets, each narrating a distinct tale of the region's terrain. Revel in the taste of sharp white wines, intense reds, and soft rosés, while taking in views of the tranquil alpine lake.",
        "Khám phá nét duyên của ẩm thực dân gian Hà Tĩnh tại Ke Go Eco Lodge. Thưởng thức rượu cần, hải sản tươi và các món đặc sản núi rừng từ các làng lân cận, mỗi bữa ăn kể câu chuyện của vùng đất và con người nơi đây.",
    ),
    (
        "Embark on an unforgettable summer trekking adventure where nature's wonders come alive! Traverse scenic trails, discovering the diverse flora and fauna of the region. With knowledgeable guides, delve into the secrets of indigenous plants and animals while soaking in panoramic mountain vistas. Experience the thrill of exploration and the serenity of nature in every step.",
        "Cùng hướng dẫn viên địa phương khám phá rừng nguyên sinh quanh hồ Kẻ Gỗ — nơi hệ động thực vật phong phú và không gian yên tĩnh xen lẫn nhịp đập của thiên nhiên. Mỗi bước đi là một trải nghiệm mới.",
    ),
    (
        "Indulge in a creative pottery class offered by the hotel, where guests delve into the fundamentals of pottery making. Learn the art of working with clay, shaping simple vases, and explore traditional coloring techniques inspired by the rich heritage of the Italian Alps. Unleash your creativity against the backdrop of stunning mountain vistas.",
        "Tham gia lớp học gốm thủ công do khách sạn tổ chức — nơi bạn tự tay tạo hình đất sét, học kỹ thuật tô màu truyền thống và khám phá di sản văn hóa gốm Hà Tĩnh trong không khí núi rừng yên tĩnh.",
    ),
    (
        "Embark on a culinary journey with our cooking class, focusing on wholesome ecological recipes inspired by the verdant valleys and alpine plateaus where fresh produce thrives in abundance. Discover the art of using locally sourced ingredients like fresh trout, succulent deer meat, and crisp mountain greens like Swiss chard and kale. Learn preservation techniques to retain the nutritional essence of these natural delicacies.",
        "Tham gia lớp học nấu ăn cùng đầu bếp địa phương — khám phá ẩm thực sinh thái từ nguyên liệu tươi xung quanh hồ Kẻ Gỗ như cá suối, rau rừng và các đặc sản vùng núi Hà Tĩnh.",
    ),
    (
        "Nestled within the Ke Go Eco Lodge area, the valleys and mountains provide exceptional trekking opportunities for the discerning traveler. Embark on scenic trails that meander through lush forests and ascend to breathtaking summits. Each path offers majestic views of serene landscapes and vibrant wildlife, ensuring an unforgettable experience. Whether you seek adventure or tranquility, the Ke Go Eco Lodge area promises unparalleled natural beauty and captivating vistas at every turn.",
        "Khu vực hồ Kẻ Gỗ mang đến những cung đường trekking xuyên rừng nguyên sinh, leo đỉnh núi và ngắm cảnh hùng vĩ. Mỗi lộ trình đều có hướng dẫn viên địa phương đồng hành, phù hợp cho cả người tìm kiếm phiêu lưu lẫn muốn tận hưởng thiên nhiên yên bình.",
    ),
    ("Ke Go Eco Lodge area's valleys and mountains offer unparalleled view for any discerned traveller", "Thung lũng và núi rừng quanh hồ Kẻ Gỗ mang đến tầm nhìn tuyệt vời cho du khách khó tính nhất"),
    ("Pristine nature and sustainable farming all around our hills and meadows", "Thiên nhiên nguyên sơ và canh tác bền vững trải dài quanh vùng đồi núi hồ Kẻ Gỗ"),
    (
        "The mountain region supports rich biodiversity, home to unique flora and fauna. Sustainable farming practices, such as grazing cows and goats, help maintain the ecological balance. These methods ensure that agriculture coexists harmoniously with nature, preserving the environment for future generations.",
        "Vùng núi hồ Kẻ Gỗ sở hữu đa dạng sinh học phong phú với hệ thực vật và động vật đặc trưng. Canh tác bền vững và chăn nuôi theo truyền thống giúp duy trì cân bằng sinh thái, bảo tồn môi trường tự nhiên cho thế hệ tương lai.",
    ),
    ("Discover enchanting villages: drive to charming hamlets for day and night adventures amidst stunning scenery", "Khám phá các bản làng quyến rũ: đi xe đến các thôn làng xinh đẹp cho những chuyến phiêu lưu ban ngày và ban đêm giữa cảnh quan hùng vĩ"),
    (
        "Cute village trails for mindful promenades and little discoveries",
        "Những con đường làng nhỏ cho những buổi dạo bộ thư thái và khám phá bất ngờ",
    ),
    # Ke Go Eco Lodge intro (about.html)
    ("Ke Go Eco Lodge is the first eco friendly boutique hotel in the locality", "Ke Go Eco Lodge là khu nghỉ sinh thái boutique đầu tiên trong vùng hồ Kẻ Gỗ, Hà Tĩnh"),
    ("Italian Alps", "vùng núi Hà Tĩnh"),
    # about.html: "In the heart of" prefix (Italian Alps was replaced → now "vùng núi Hà Tĩnh")
    ("In the heart of vùng núi Hà Tĩnh", "Giữa lòng vùng núi hồ Kẻ Gỗ, Hà Tĩnh"),
    # area.html: village description
    (
        "Nestled in a picturesque valley ensconced by majestic mountains, Kẻ Gỗ is a quaint village where tradition thrives. Its vibrant markets beckon with locally crafted treasures, from intricately woven textiles to exquisitely carved wooden artifacts. Visitors revel in the artistry of pottery, leatherwork, and vibrant tapestries, each telling a tale of Kẻ Gỗ's rich cultural heritage.",
        "Nằm trong thung lũng thơ mộng bao quanh bởi núi rừng hùng vĩ, làng Kẻ Gỗ là nơi truyền thống vẫn còn sống. Chợ phiên nhộn nhịp với đồ thủ công địa phương — từ vải dệt truyền thống đến gốm sứ và tác phẩm điêu khắc gỗ — mỗi món đều kể câu chuyện văn hóa phong phú của vùng đất này.",
    ),
    # gallery.html: partially-translated wine/Italian Alps paragraph (Discover→Khám phá already applied)
    (
        "Khám phá the allure of the wine traditions in the vùng núi Hà Tĩnh at our exclusive hotel, nestled amongst stunning mountain vistas. Enjoy an expertly chosen array of local wines from neighboring hamlets, each narrating a distinct tale of the region's terrain. Revel in the taste of sharp white wines, intense reds, and soft rosés, while taking in views of the tranquil alpine lake.",
        "Khám phá nét duyên của ẩm thực dân gian Hà Tĩnh tại Ke Go Eco Lodge. Thưởng thức rượu cần, hải sản tươi và các món đặc sản núi rừng từ các làng lân cận, mỗi bữa ăn kể câu chuyện của vùng đất và con người nơi đây.",
    ),
    # index.html: restaurant description
    (
        "Savour the gastronomic pleasures of contemporary ẩm thực địa phương at our eating establishments, where each recipe marries novelty and heritage. Amplify your experience with our swanky and inventive mixed drinks, meticulously concocted to pair with our wide range of high-quality wines at our chic lounge.",
        "Thưởng thức ẩm thực địa phương tại nhà hàng Ke Go Eco Lodge, nơi mỗi món ăn kết hợp hương vị mới lạ và di sản ẩm thực Hà Tĩnh. Hoàn thiện trải nghiệm bằng cocktail sáng tạo và rượu cần truyền thống tại khu lounge ven hồ.",
    ),
    # contact.html: form instruction
    ("Fill out this form and we will aim to respond as soon as possible", "Điền vào biểu mẫu này và chúng tôi sẽ phản hồi trong thời gian sớm nhất"),
    # events.html: body copy
    (
        "Enjoy the ideal serene surroundings to pamper your senses and attain a harmonious mind and spirit. We focus on mindful approach towards operating our business and treating our customers",
        "Tận hưởng không gian yên tĩnh lý tưởng để chăm sóc cảm giác và đạt được sự hài hòa giữa tâm trí và tinh thần. Chúng tôi hướng tới cách tiếp cận có ý thức trong mọi hoạt động và trong cách phục vụ khách hàng",
    ),
    # restaurants.html: placeholder body
    (
        "Some text about the restaurant and food, where every moment is a masterpiece of natural beauty. Embrace serenity amidst breathtaking views of towering mountains and tranquil waters",
        "Nhà hàng Ke Go Eco Lodge phục vụ ẩm thực địa phương Hà Tĩnh trong không gian thiên nhiên nguyên sơ, nơi mỗi bữa ăn là khoảnh khắc kết nối với rừng núi và mặt hồ yên tĩnh",
    ),
]

HOTALE_UPLOAD_MAP = {
    "upload/Group-40.png": "assets/max-themes.net/demos/hotale/hotale/resort/upload/Group-40.png",
    "upload/play.png": "assets/max-themes.net/demos/hotale/hotale/resort/upload/play.png",
    "upload/about-2-icon-1.png": "assets/max-themes.net/demos/hotale/hotale/resort/upload/about-2-icon-1.png",
    "upload/about-2-icon-2.png": "assets/max-themes.net/demos/hotale/hotale/resort/upload/about-2-icon-2.png",
    "upload/about-2-icon-3.png": "assets/max-themes.net/demos/hotale/hotale/resort/upload/about-2-icon-3.png",
    "upload/about-2-icon-4.png": "assets/max-themes.net/demos/hotale/hotale/resort/upload/about-2-icon-4.png",
    "upload/about-2-icon-5.png": "assets/max-themes.net/demos/hotale/hotale/resort/upload/about-2-icon-5.png",
    "upload/about-2-icon-6-1.png": "assets/max-themes.net/demos/hotale/hotale/resort/upload/about-2-icon-6-1.png",
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

HOTALE_IMG_POOL = [
    "08_hospitality_hospitality_beachfront_resort.png",
    "15_hospitality_luxury_resort_pool_sunset.png",
    "09_hospitality_hospitality_sea_view_room.png",
    "29_hospitality_luxury_sea_view_room.png",
    "26_hospitality_beach_restaurant_sunset.png",
    "48_hospitality_beach_resort_golden_hour.png",
]

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
    # luxestay rooms/restaurant EN headings
    ("Serene spaces,", "Không gian yên tĩnh,"),
    ("Our rooms are equipped with everything you need", "Mỗi phòng được trang bị đầy đủ tiện nghi"),
    ("Authentic ", "Ẩm thực địa phương "),
    ("An intimate dining experience", "Trải nghiệm ẩm thực tinh tế"),
    (">Our menu<", ">Thực đơn<"),
    # Eden Hotel (Bali/Kuta) meta description leftover from scrape
    (
        "Located right at the heart of Central Kuta, Eden Hotel offers a four-stars scenic getaway to nature. Only minutes away from the Kuta Beach.",
        "Tọa lạc ven bờ biển Thiên Cầm, LuxeStay Hà Tĩnh mang đến không gian nghỉ dưỡng hiện đại, yên tĩnh và gần biển.",
    ),
    # luxestay homepage body copy
    (
        "Step outside and Hà Tĩnh begins - temples, waterfalls, rice fields, and coastline, all within reach",
        "Bước ra ngoài là Hà Tĩnh — chùa chiền, thác nước, đồng lúa và bờ biển, tất cả đều gần tầm tay",
    ),
    (
        "Built in Hà Tĩnh in 2018, LuxeStay Ha Tinh is a 32-room retreat where the island does the talking and guests keep coming back to listen.",
        "Thành lập tại Hà Tĩnh năm 2018, LuxeStay Hà Tĩnh là khu nghỉ dưỡng ven biển nơi thiên nhiên cất tiếng và du khách tìm về mỗi mùa hè.",
    ),
    (
        "Luxestay Ha Tinh is a 32-room retreat where the island does the talking and guests keep coming back to listen.",
        "LuxeStay Hà Tĩnh là khu nghỉ dưỡng ven biển với không gian được thiết kế để lắng nghe tiếng biển và trở về mỗi mùa hè.",
    ),
    ("More than a way, a complete escape", "Hơn cả một kỳ nghỉ — là lối thoát hoàn toàn"),
    # luxestay rooms.html: English amenity descriptions
    ("Step outside into your own private balcony and enjoy peaceful views, fresh air, and quiet moments of relaxation.", "Bước ra ban công riêng tư, đón gió nhẹ và tận hưởng tầm nhìn yên bình trong những khoảnh khắc thư giãn trọn vẹn."),
    ("Unwind on a plush king-size bed with premium linens, designed for deep rest and uninterrupted sleep.", "Nghỉ ngơi trên giường king-size đệm êm với ga trải cao cấp, thiết kế cho giấc ngủ sâu và không bị gián đoạn."),
    ("Wake up to calming views of nature or the surrounding landscape, thoughtfully framed from your room.", "Thức dậy với tầm nhìn thư giãn — thiên nhiên hoặc cảnh quan xung quanh được bố cục tinh tế từ căn phòng."),
    ("Enjoy your favorite content with a smart TV, high-speed Wi-Fi, and seamless in-room connectivity.", "Thưởng thức nội dung yêu thích với TV thông minh, Wi-Fi tốc độ cao và kết nối liền mạch trong phòng."),
    ("Refresh in a contemporary bathroom featuring a rain shower, luxury toiletries, and soft towels.", "Sảng khoái trong phòng tắm hiện đại với vòi sen mưa, nước hoa phòng tắm cao cấp và khăn mềm mại."),
    # luxestay wellness.html: English body copy
    ("A Sanctuary of Stillness, Restoration &amp; Deep Relaxation", "Không gian tĩnh lặng, phục hồi &amp; thư giãn sâu"),
    ("At LuxeStay Ha Tinh Spa, we believe restoration is not a luxury - it is a necessity.", "Tại LuxeStay Ha Tinh Spa, chúng tôi tin rằng phục hồi không phải xa xỉ — đó là nhu cầu thiết yếu."),
    ("Ancient traditions, thoughtfully refined.", "Truyền thống cổ xưa, được chắt lọc tinh tế."),
    ("A one-to-one session with our resident yoga teacher, tailored entirely to your body, goals, and current state. Choose your setting", "Buổi yoga riêng tư với giáo viên thường trú — thiết kế hoàn toàn theo cơ thể, mục tiêu và trạng thái của bạn. Chọn không gian"),
    ("A guided session combining pranayama breathing techniques with seated meditation. Practiced in our dedicated meditation room with curated soundscapes and essential oil diffusion. Offered individually or for two.", "Buổi thiền hướng dẫn kết hợp kỹ thuật thở pranayama trong phòng thiền chuyên dụng với âm thanh thiên nhiên và tinh dầu thơm. Dành cho cá nhân hoặc cặp đôi."),
    ("A flowing, breath-led vinyasa practice held in the open-air pavilion at first light. Each session is sequenced to the season", "Lớp yoga vinyasa theo hơi thở tại nhà sàn ngoài trời lúc bình minh — được thiết kế theo mùa"),
    ("A shared ritual for two guests in our private couples suite", "Nghi lễ thư giãn cho hai người trong không gian couples suite riêng tư"),
    ("Slow, deliberate deep-tissue work focused on the areas most affected by tension. Combined with guided breathwork to help the nervous system release what hands alone cannot reach.", "Liệu pháp deep-tissue chậm rãi, tập trung vào các vùng căng thẳng nhất. Kết hợp hướng dẫn thở để hệ thần kinh thả lỏng những gì bàn tay không thể chạm tới."),
    ("River-warmed basalt stones trace the spine and dissolve chronic tension while the therapist works with long, grounding strokes. A restorative choice for guests arriving after long travel or carrying physical stress.", "Đá bazan hấp nóng lần theo cột sống, tan dần sức căng mãn tính trong khi chuyên viên trị liệu thực hiện các đường vuốt dài, vững chắc. Lý tưởng cho khách vừa kết thúc hành trình dài."),
    ("A warm botanical scrub followed by a full-body oil massage with sandalwood, neroli, and frankincense. Ends with a cool compress and guided stillness.", "Tẩy da chết thảo mộc ấm áp, tiếp theo là massage toàn thân với tinh dầu đàn hương, neroli và nhũ hương. Kết thúc bằng khăn mát và hướng dẫn tĩnh tâm."),
    # luxestay wellness hero heading
    (
        'Rejuvenate <br class="framer-text">your soul',
        'Phục hồi <br class="framer-text">tâm hồn',
    ),
    # luxestay room type headings
    ("Family room", "Phòng gia đình"),
    ("Executive room", "Phòng Executive"),
    ("Deluxe room", "Phòng Deluxe"),
    ("Premium suite", "Suite cao cấp"),
    ("Super Executive room", "Phòng Super Executive"),
    ("Other accommodations", "Phòng khác"),
    # luxestay wedding heading mix
    ("Kỷ niệm tình yêu in Extraordinary Settings", "Kỷ niệm tình yêu trong không gian đặc biệt"),
    # luxestay wellness headings
    ("Organic well being", "Sức khỏe toàn diện"),
    ("Our treatments", "Liệu pháp của chúng tôi"),
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
#__framer-badge-container,#__framer-badge-container *,.__framer-badge,.framer-badge,
body>div[style*="position: fixed"][style*="bottom"],a[href*="framer.com/edit"]{display:none!important;visibility:hidden!important}
</style>"""

FRAMER_BADGE_SCRIPT = """<script id="framer-badge-cleanup">
setInterval(()=>document.querySelectorAll('#__framer-badge-container,.__framer-badge,.framer-badge').forEach(el=>el.remove()),500);
</script>"""

FRAMER_LOGO_SVG = (
    "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='240' height='72' viewBox='0 0 240 72'%3E"
    "%3Crect width='240' height='72' rx='10' fill='%2310423A'/%3E"
    "%3Ctext x='24' y='44' font-family='Arial,sans-serif' font-size='22' font-weight='700' fill='white'%3EH%C3%A0%20T%C4%A9nh%3C/text%3E"
    "%3C/svg%3E"
)

MOUNTAIN_STATIC_HERO = f"""
<section id="mountain-static-hero" style="position:relative;z-index:20;min-height:92vh;background:linear-gradient(90deg,rgba(18,17,19,.72),rgba(18,17,19,.22)),url('../assets/shared-images/10_experience_experience_ke_go_boat_tour.png') center/cover no-repeat;color:#fff;display:flex;align-items:flex-end;padding:clamp(32px,7vw,96px);box-sizing:border-box">
  <header style="position:absolute;z-index:50;left:clamp(24px,5vw,72px);right:clamp(24px,5vw,72px);top:24px;display:flex;align-items:center;justify-content:space-between;gap:24px;padding:14px 18px;border-radius:999px;background:rgba(18,17,19,.34);backdrop-filter:blur(12px);font:700 13px/1 Arial,sans-serif;letter-spacing:.02em">
    <a href="index.html" style="color:#fff;text-decoration:none;display:inline-flex;align-items:center;gap:10px"><span style="width:28px;height:28px;border-radius:50%;background:#688683;display:inline-block"></span><span>Ke Go Eco Lodge</span></a>
    <nav style="display:flex;align-items:center;gap:22px;flex-wrap:wrap"><a href="rooms.html" style="color:#fff;text-decoration:none">Phòng</a><a href="about.html" style="color:#fff;text-decoration:none">Giới thiệu</a><a href="contact.html" style="color:#fff;text-decoration:none">Liên hệ</a><a href="rooms.html" style="color:#101113;text-decoration:none;background:#e4e6c3;border-radius:999px;padding:12px 16px">Đặt phòng</a></nav>
  </header>
  <div style="max-width:820px">
    <p style="font:700 14px/1.2 Arial,sans-serif;letter-spacing:0;text-transform:uppercase;margin:0 0 18px;color:#e4e6c3">Ke Go Eco Lodge</p>
    <h1 style="font:700 clamp(46px,7vw,92px)/.95 Georgia,serif;letter-spacing:0;margin:0 0 24px">Nghỉ dưỡng giữa rừng hồ Kẻ Gỗ</h1>
    <p style="font:400 20px/1.6 Arial,sans-serif;max-width:620px;margin:0 0 30px;color:#f7f7f0">Không gian lodge yên tĩnh cho chuyến nghỉ cuối tuần, workshop và trải nghiệm thiên nhiên tại Hà Tĩnh.</p>
    <a href="rooms.html" style="display:inline-flex;align-items:center;min-height:48px;padding:0 24px;border:1px solid #e4e6c3;border-radius:999px;color:#fff;text-decoration:none;font:700 14px/1 Arial,sans-serif">Xem phòng</a>
  </div>
</section>
"""

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

GLOBAL_LEFTOVERS = [
    ("Bali", "Hà Tĩnh"),
    ("Italy", "Hà Tĩnh"),
    ("Europe", "Hà Tĩnh"),
    ("Madrid", "Thiên Cầm"),
    ("Spain", "Thiên Cầm"),
    ("Indonesia", "Đồng Lộc"),
    ("Egypt", "Hương Tích"),
    ("Arcosa", "Kẻ Gỗ"),
]


def p(name: str) -> str:
    return f"{IMG}/{name}"


def inject_head(html: str, snippet: str, marker: str) -> str:
    if marker in html:
        pattern = rf'<style id="{re.escape(marker)}">[\s\S]*?</style>'
        html = re.sub(pattern, "", html, count=1)
    return html.replace("</head>", snippet + "</head>", 1)


def fix_crawl_artifacts(html: str) -> str:
    html = html.replace("index.htmlassets/", "assets/")
    html = html.replace("index.htmljs/", "assets/preview.colorlib.com/theme/deluxe/js/")
    html = html.replace('src="/assets/', 'src="assets/')
    html = html.replace('href="/assets/', 'href="assets/')
    html = html.replace('url("/assets/', 'url("assets/')
    html = html.replace("url('/assets/", "url('assets/")
    html = html.replace("url(&quot;/assets/", "url(&quot;assets/")
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
    html = inject_head(html, COLORLIB_LAYOUT_FIX, "colorlib-layout-fix")
    for old, new in COLORLIB_VI:
        html = html.replace(old, new)
    for old, new in COLORLIB_VI_EXTRA:
        html = html.replace(old, new)
    html = re.sub(
        r"On her way she met a copy\.[\s\S]{0,800}?safe country\.",
        "Nhà hàng Deluxe Hotel phục vụ hải sản và đặc sản Hà Tĩnh trong không gian ven biển Thiên Cầm.",
        html,
    )
    html = re.sub(r"Little Blind Text", "nội dung demo", html)
    html = re.sub(r"Lorem ipsum[^<]{0,400}", "Nội dung demo phù hợp khách sạn Hà Tĩnh.", html)
    html = re.sub(
        r"Deluxe Hotel Ha Tinh,[^<]*Bookmarksgrove[^<]*continued her way\.",
        "Khong gian luu tru duoc sap xep gon gang, co khu am thuc, dich vu ho tro va cac hang phong phu hop cho chuyen nghi tai Ha Tinh.",
        html,
    )
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
    html = re.sub(
        r'(<img\b[^>]*alt="Company logo"[^>]*\bsrc=")[^"]+(")',
        rf"\1{FRAMER_LOGO_SVG}\2",
        html,
        flags=re.I,
    )
    html = re.sub(
        r'(<link\b[^>]*\bhref=")assets/framerusercontent\.com/images/[^"]+\.(?:png|svg)([^"]*"[^>]*\brel="(?:icon|apple-touch-icon)"[^>]*>)',
        rf"\1{FRAMER_LOGO_SVG}\2",
        html,
        flags=re.I,
    )
    html = re.sub(
        r'(<link\b[^>]*\brel="(?:icon|apple-touch-icon)"[^>]*\bhref=")assets/framerusercontent\.com/images/[^"]+\.(?:png|svg)([^"]*"[^>]*>)',
        rf"\1{FRAMER_LOGO_SVG}\2",
        html,
        flags=re.I,
    )
    html = re.sub(
        r'(src|href)="assets/framerusercontent\.com/images/[^"]+\.svg[^"]*"',
        lambda m: f'{m.group(1)}="{FRAMER_LOGO_SVG}"',
        html,
        flags=re.I,
    )
    html = re.sub(r'\s+srcset="[^"]*"', "", html)
    html = inject_head(html, FRAMER_HIDE, "framer-hide-vendor")
    if "framer-badge-cleanup" not in html:
        html = html.replace("</body>", FRAMER_BADGE_SCRIPT + "</body>", 1)
    return html


def fix_framer_imgs(html: str, pool: list[str]) -> str:
    idx = 0

    def next_img() -> str:
        nonlocal idx
        path = p(pool[idx % len(pool)])
        idx += 1
        return path

    def src_repl(_m: re.Match) -> str:
        return f'src="{next_img()}"'

    def href_repl(_m: re.Match) -> str:
        return f'href="{next_img()}"'

    def url_repl(_m: re.Match) -> str:
        return f"url('{next_img()}')"

    def url_quot_repl(_m: re.Match) -> str:
        return f'url(&quot;{next_img()}&quot;)'

    pat = r"(?:https://|assets/)?framerusercontent\.com/images/[^\"')]+\.(?:jpg|jpeg|png|webp)[^\"')]*"
    html = re.sub(rf'src="({pat})"', src_repl, html, flags=re.I)
    html = re.sub(rf'href="({pat})"', href_repl, html, flags=re.I)
    html = re.sub(rf"url\((['\"]?)({pat})\1\)", url_repl, html, flags=re.I)
    html = re.sub(rf"url\(&quot;({pat})&quot;\)", url_quot_repl, html, flags=re.I)
    html = re.sub(
        r"assets/framerusercontent\.com/images/[^\"')<\s]+\.(?:jpg|jpeg|png|webp)[^\"')<\s]*",
        lambda _m: next_img(),
        html,
        flags=re.I,
    )
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
    html = fix_framer_imgs(html, MOUNTAIN_IMG_POOL)
    for old, new in MOUNTAIN_VI_EXTRA:
        html = html.replace(old, new)
    return html


def inject_mountain_static_hero(html: str) -> str:
    if "mountain-static-hero" in html:
        return re.sub(
            r'<section id="mountain-static-hero"[\s\S]*?</section>',
            MOUNTAIN_STATIC_HERO,
            html,
            count=1,
            flags=re.I,
        )
    return re.sub(r"(<body\b[^>]*>)", r"\1" + MOUNTAIN_STATIC_HERO, html, count=1, flags=re.I)


def _apply_vi_list(html: str, pairs: list[tuple[str, str]]) -> str:
    for old, new in pairs:
        html = html.replace(old, new)
    return html


def fix_framer_text_asset(text: str) -> str:
    text = _apply_vi_list(text, FRAMER_VI)
    text = _apply_vi_list(text, FRAMER_VI_EXTRA)
    text = _apply_vi_list(text, MOUNTAIN_VI)
    text = _apply_vi_list(text, MOUNTAIN_VI_EXTRA)
    text = _apply_vi_list(text, LUXESTAY_VI)
    return text


def _moonlit_is_regex(pat: str) -> bool:
    return pat.startswith("(") or "\\" in pat or "(?:" in pat or pat.endswith("+")


def fix_moonlit(html: str) -> str:
    html = fix_crawl_artifacts(html)
    for old, new in MOONLIT_VI:
        if _moonlit_is_regex(old):
            html = re.sub(old, new, html)
        else:
            html = html.replace(old, new)
    for old, new in MOONLIT_VI_EXTRA:
        html = html.replace(old, new)
    html = re.sub(
        r"Welcome to Career Compass,[\s\S]{0,650}?tools you need to succeed\.",
        "Moonlit chia sẻ kinh nghiệm lưu trú, gợi ý lịch trình và những lựa chọn nghỉ dưỡng phù hợp cho chuyến đi Hà Tĩnh. Nội dung demo tập trung vào trải nghiệm thực tế: phòng nghỉ, ẩm thực địa phương và các hoạt động ven biển Thiên Cầm.",
        html,
    )
    html = re.sub(
        r"Welcome to Career Compass,[^<]+job market\.",
        "Moonlit chia sẻ kinh nghiệm lưu trú, gợi ý lịch trình và những lựa chọn nghỉ dưỡng phù hợp cho chuyến đi Hà Tĩnh.",
        html,
    )
    html = re.sub(
        r"At Career Compass,[\s\S]{0,520}?tools you need to succeed\.",
        "Đội ngũ Moonlit luôn cập nhật dịch vụ để khách có kỳ nghỉ gọn gàng, thoải mái và dễ sắp xếp. Từ đặt phòng, đưa đón đến gợi ý ăn uống, mọi thông tin được trình bày ngắn gọn để khách dễ chọn.",
        html,
    )
    html = re.sub(
        r"Contrary to popular belief,[\s\S]{0,340}?Virginia",
        "Một kỳ nghỉ đáng nhớ thường đến từ những chi tiết nhỏ: phòng sạch, bữa sáng vừa miệng, lịch trình vừa đủ và đội ngũ phục vụ đúng lúc.",
        html,
    )
    html = re.sub(
        r"I still have a lot of studying to do[\s\S]{0,240}?later time\.",
        "Phòng sạch, vị trí thuận tiện và nhân viên hỗ trợ nhanh. Đây là lựa chọn phù hợp cho chuyến nghỉ ngắn tại Hà Tĩnh.",
        html,
    )
    html = html.replace("classHọ tên", "className")
    html = html.replace("t.Danh mục", "t.category")
    html = html.replace("Leave a Bình luận", "Gửi bình luận")
    html = html.replace("Submit Bình luận", "Gửi bình luận")
    html = html.replace("Your Bình luận", "Nội dung bình luận")
    html = html.replace("Your Họ tên", "Họ tên")
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
    moonlit_bg = p("17_hospitality_modern_beach_hotel_exterior.png")
    html = html.replace("assets/images/pages/header__bg.webp", moonlit_bg)
    html = html.replace("assets/images/pages/blog/1.webp", p("07_experience_experience_local_seafood.png"))
    html = html.replace("assets/images/pages/blog/2.webp", p("22_experience_seafood_table_beach.png"))
    html = html.replace("assets/images/pages/blog/3.webp", p("44_experience_seafood_dinner_beach.png"))
    html = html.replace('src="assets/images/video/Moonlit.mp4"', f'poster="{p("11_hero_wide_beach_sunrise_boats.png")}"')
    html = re.sub(
        r"assets/images/pages/blog/[0-9]+\.webp",
        p("07_experience_experience_local_seafood.png"),
        html,
    )
    html = html.replace("assets/images/favicon.ico", "../assets/shared-images/08_hospitality_hospitality_beachfront_resort.png")
    html = html.replace("assets/moonlit-react.netlify.app/assets/images/favicon.ico", "../assets/shared-images/08_hospitality_hospitality_beachfront_resort.png")
    html = html.replace("assets/moonlit-react.netlify.app/../assets/shared-images/", "../assets/shared-images/")
    html = html.replace("callto:#", "tel:+842393681888")
    html = html.replace("callto:121", "tel:+842393681888")
    html = re.sub(r'href="index\.html(?:winter-activities|summer-activities|cultural-tours|cart|room2/[0-9]+)"', 'href="#"', html)
    html = html.replace("/room-two", "room-two.html")
    html = html.replace("/room-one", "room-one.html")
    html = html.replace("KhÃ¡m phÃ¡ More", "Xem thÃªm")
    html = html.replace("Load More", "Xem thÃªm")
    html = html.replace("always ready to tackle new challenges with and expertise.Their commitment to and delivering tailored.", "với dịch vụ chu đáo, phòng nghỉ tiện nghi và vị trí thuận lợi.")
    html = html.replace("A step up from the standard room, often with better views, more space, and additional amenities.", "Phòng rộng rãi, tiện nghi, phù hợp cho kỳ nghỉ tại Hà Tĩnh.")
    html = re.sub(r'<div class="gdpr-cookie-banner">[\s\S]*?</div>', "", html)
    html = re.sub(r"Cookies enable you to use shopping carts[\s\S]{0,400}?web searches\.", "", html)
    html = inject_head(html, MOONLIT_ICON_FALLBACK, "moonlit-icon-fallback")
    html = inject_head(html, MOONLIT_LAYOUT_FIX, "moonlit-layout-fix")
    return html


def fix_moonlit_text_asset(text: str) -> str:
    for old, new in MOONLIT_VI_EXTRA:
        text = text.replace(old, new)
    text = re.sub(
        r"Welcome to Career Compass,[\s\S]{0,650}?tools you need to succeed\.",
        "Moonlit chia sẻ kinh nghiệm lưu trú, gợi ý lịch trình và những lựa chọn nghỉ dưỡng phù hợp cho chuyến đi Hà Tĩnh. Nội dung demo tập trung vào trải nghiệm thực tế: phòng nghỉ, ẩm thực địa phương và các hoạt động ven biển Thiên Cầm.",
        text,
    )
    text = re.sub(
        r"Welcome to Career Compass,[^\"`]+job market\.",
        "Moonlit chia sẻ kinh nghiệm lưu trú, gợi ý lịch trình và những lựa chọn nghỉ dưỡng phù hợp cho chuyến đi Hà Tĩnh.",
        text,
    )
    text = re.sub(
        r"At Career Compass,[\s\S]{0,520}?tools you need to succeed\.",
        "Đội ngũ Moonlit luôn cập nhật dịch vụ để khách có kỳ nghỉ gọn gàng, thoải mái và dễ sắp xếp. Từ đặt phòng, đưa đón đến gợi ý ăn uống, mọi thông tin được trình bày ngắn gọn để khách dễ chọn.",
        text,
    )
    text = re.sub(
        r"Contrary to popular belief,[\s\S]{0,340}?Virginia",
        "Một kỳ nghỉ đáng nhớ thường đến từ những chi tiết nhỏ: phòng sạch, bữa sáng vừa miệng, lịch trình vừa đủ và đội ngũ phục vụ đúng lúc.",
        text,
    )
    text = re.sub(
        r"I still have a lot of studying to do[\s\S]{0,240}?later time\.",
        "Phòng sạch, vị trí thuận tiện và nhân viên hỗ trợ nhanh. Đây là lựa chọn phù hợp cho chuyến nghỉ ngắn tại Hà Tĩnh.",
        text,
    )
    text = text.replace("classHọ tên", "className")
    text = text.replace("attributeHọ tênspace", "attributeNamespace")
    text = text.replace("attributeHọ tên", "attributeName")
    text = text.replace("propertyHọ tên", "propertyName")
    text = text.replace("displayHọ tên", "displayName")
    text = text.replace("nodeHọ tên", "nodeName")
    text = text.replace("cookieHọ tên", "cookieName")
    text = text.replace("t.Danh mục", "t.category")
    text = text.replace("Leave a Bình luận", "Gửi bình luận")
    text = text.replace("Submit Bình luận", "Gửi bình luận")
    text = text.replace("Your Bình luận", "Nội dung bình luận")
    text = text.replace("Your Họ tên", "Họ tên")
    return text


def write_processed(dst: Path, html: str) -> None:
    dst.write_text(process_html(dst, html), encoding="utf-8")


def repair_placeholder_routes() -> int:
    count = 0

    colorlib = ROOT / "colorlib-deluxe"
    room_single = colorlib / "room-single.html"
    rooms = colorlib / "rooms.html"
    if room_single.exists() and rooms.exists():
        current = room_single.read_text(encoding="utf-8", errors="ignore")
        if "Not Found" in current or len(current) < 2000:
            html = rooms.read_text(encoding="utf-8", errors="ignore")
            html = html.replace("<title>Deluxe Hotel Ha Tinh — Lưu trú tiện nghi</title>", "<title>Chi tiết phòng — Deluxe Hotel Ha Tinh</title>")
            html = html.replace('<h1 class="mb-4 bread">Phòng</h1>', '<h1 class="mb-4 bread">Chi tiết phòng</h1>')
            write_processed(room_single, html)
            count += 1

    moonlit = ROOT / "moonlit-react"
    moonlit_fallbacks = {
        "home.html": "index.html",
        "restaurant.html": "resturant.html",
        "room-details-1.html": "room_1.html",
        "room-details-2.html": "room_2.html",
        "home-dark_contact.html": "contact.html",
        "home-video_contact.html": "contact.html",
    }
    for name, fallback in moonlit_fallbacks.items():
        dst = moonlit / name
        src = moonlit / fallback
        if not dst.exists() or not src.exists():
            continue
        current = dst.read_text(encoding="utf-8", errors="ignore")
        if len(current) < 4000 or '<div id="root"></div>' in current:
            html = src.read_text(encoding="utf-8", errors="ignore")
            html = html.replace(f'href="{fallback}"', f'href="{name}"')
            write_processed(dst, html)
            count += 1

    return count


def fix_hotale_uploads(html: str) -> str:
    html = inject_head(html, HOTALE_POLISH, "hotale-polish")
    for old, new in HOTALE_UPLOAD_MAP.items():
        html = html.replace(old, new)
        html = html.replace(f"assets/max-themes.net/demos/hotale/hotale/resort/{old}", new)
    html = html.replace(
        "assets/max-themes.net/demos/hotale/hotale/resort/../assets/shared-images/",
        "../assets/shared-images/",
    )
    html = re.sub(
        r'<img src="[^"]+"([^>]*title="Group 40"[^>]*)>',
        r'<img src="assets/max-themes.net/demos/hotale/hotale/resort/upload/Group-40.png"\1>',
        html,
        flags=re.I,
    )
    idx = 0

    def next_img() -> str:
        nonlocal idx
        path = p(HOTALE_IMG_POOL[idx % len(HOTALE_IMG_POOL)])
        idx += 1
        return path

    def upload_attr_repl(m: re.Match) -> str:
        src = m.group(2)
        low = src.lower()
        if any(x in low for x in ("logo", "icon", "favicon", "map-marker", "group-40", "play.png", "group-36", "footer-cards")):
            return m.group(0)
        return f'{m.group(1)}"{next_img()}"'

    html = re.sub(
        r'((?:src|href)=)"(upload/[^"]+\.(?:jpg|jpeg|png|webp))"',
        upload_attr_repl,
        html,
        flags=re.I,
    )
    html = re.sub(
        r'url\((["\']?)(upload/[^"\')]+\.(?:jpg|jpeg|png|webp))\1\)',
        lambda _m: f"url('{next_img()}')",
        html,
        flags=re.I,
    )
    html = re.sub(
        r"url\(&quot;upload/[^&]+?\.(?:jpg|jpeg|png|webp)&quot;\)",
        lambda _m: f"url(&quot;{next_img()}&quot;)",
        html,
        flags=re.I,
    )
    html = re.sub(
        r'"upload/[^"]+\.(?:jpg|jpeg|png|webp)"',
        lambda _m: f'"{next_img()}"',
        html,
        flags=re.I,
    )
    for old, new in HOTALE_VI:
        html = html.replace(old, new)
    html = html.replace("Kỳ nghỉ ven biển trọn vẹn tại Thiên Cầm", "Resort Hà Tĩnh")
    html = html.replace("Nghỉ dưỡng ven biển Thiên Cầm", "Resort Hà Tĩnh")
    html = html.replace("Resort biển Thiên Cầm", "Resort Hà Tĩnh")
    html = re.sub(
        r'(<input\b[^>]*class="[^"]*\btourmaster-room-search-submit\b[^"]*"[^>]*\bvalue=")[^"]+(")',
        r"\1Tìm phòng\2",
        html,
        flags=re.I,
    )
    html = re.sub(
        r"Bên bờ biển Thiên Cầm,\s*far from the countries Hà Tĩnh,\s*có những trải nghiệm nghỉ dưỡng yên tĩnh\.\s*Separated they live in Thiên Cầm right at the coast of(?: the)?",
        "Bên bờ biển Thiên Cầm, du khách có thể nghỉ ngơi trong không gian yên tĩnh, gần biển và thuận tiện khám phá Hà Tĩnh",
        html,
    )
    html = html.replace("far from the countries Hà Tĩnh, ", "")
    html = html.replace("Separated they live in Thiên Cầm right at the coast of the", "Không gian nghỉ dưỡng yên tĩnh tại Hà Tĩnh")
    html = html.replace("Separated they live in Thiên Cầm right at the coast of", "Không gian nghỉ dưỡng yên tĩnh tại Hà Tĩnh")
    html = html.replace("Separated they live in Thiên Cầm right at the", "Không gian nghỉ dưỡng nằm gần bờ biển")
    html = html.replace("here live the blind texts. Separated they live in Bookm", "không gian yên tĩnh cho kỳ nghỉ Thiên Cầm")
    html = html.replace("arksgrove right at the coast of the Semantics, a large language ocean. A small", "")
    return html


def fix_asatha_assets(html: str) -> str:
    idx = 0

    def next_img() -> str:
        nonlocal idx
        path = p(ASATHA_IMG_POOL[idx % len(ASATHA_IMG_POOL)])
        idx += 1
        return path

    def img_repl(m: re.Match) -> str:
        src = m.group(1)
        if "logo" in src.lower() or src.endswith(".svg"):
            return m.group(0)
        return f'src="{next_img()}"'

    html = re.sub(
        r'src="(assets/cdn\.prod\.website-files\.com/[^"]+\.(?:webp|jpg|jpeg|png))"',
        img_repl,
        html,
    )
    html = re.sub(
        r'data-poster-url="assets/cdn\.prod\.website-files\.com/[^"]+\.(?:jpg|jpeg|png|webp)"',
        lambda _m: f'data-poster-url="{next_img()}"',
        html,
        flags=re.I,
    )
    html = re.sub(
        r'data-video-urls="assets/cdn\.prod\.website-files\.com/[^"]+"',
        'data-video-urls=""',
        html,
        flags=re.I,
    )
    html = re.sub(
        r'background-image:url\(&quot;assets/cdn\.prod\.website-files\.com/[^&]+?\.(?:jpg|jpeg|png|webp)&quot;\)',
        lambda _m: f'background-image:url(&quot;{next_img()}&quot;)',
        html,
        flags=re.I,
    )
    html = re.sub(
        r'<source src="assets/cdn\.prod\.website-files\.com/[^"]+\.(?:mp4|webm)" data-wf-ignore="true">',
        "",
        html,
        flags=re.I,
    )
    html = re.sub(r'\s+srcset="assets/cdn\.prod\.website-files\.com/[^"]*"', "", html)
    html = html.replace(
        "Where time slows, <em>Comfort deepens</em>",
        "Nơi thời gian chậm lại, <em>An lạc sâu thêm</em>",
    )
    html = html.replace(
        "Every space is more than a room; it’s a sanctuary where comfort, privacy, and style meet.",
        "Mỗi không gian là một ốc đảo riêng tư — tiện nghi, cảnh quan và dịch vụ hoà quyện.",
    )
    html = html.replace(
        'Escape to <em class="wood-700-text">Bliss.</em>',
        'Tìm lại bình yên tại <em class="wood-700-text">Kẻ Gỗ.</em>',
    )
    html = html.replace(
        "Introduce your luxury retreat with story, gallery, and amenities. This  template page highlights brand heritage, spa culture, and guest experience.",
        "Ke Go Retreat — không gian nghỉ dưỡng ven hồ Kẻ Gỗ, Hà Tĩnh. Thiết kế gắn kết thiên nhiên nguyên sơ và tiện nghi hiện đại.",
    )
    html = html.replace(
        "We envisioned more than a resort. We created a haven where nature’s raw beauty and modern comfort exist in effortless harmony. Every villa, every pathway, every view is crafted to let you reconnect with yourself, your loved ones, and the timeless spirit.",
        "Ke Go Retreat không chỉ là nơi lưu trú — đây là không gian để bạn thực sự nghỉ ngơi. Mỗi không gian được thiết kế gắn với thiên nhiên hồ Kẻ Gỗ, để bạn chạm vào sự yên tĩnh hiếm có giữa rừng núi Hà Tĩnh.",
    )
    html = html.replace(
        "Your dream retreat at Ke Go Retreat is just a conversation away.",
        "Chuyến nghỉ dưỡng tại Ke Go Retreat của bạn chỉ cách một cuộc gọi.",
    )
    # about-us: mixed prefix + English body copy
    html = html.replace(
        "Khám phá sự cân bằng giữa sang trọng và thiên nhiên tại Ke Go Retreat.you.",
        "Khám phá sự cân bằng giữa sang trọng và thiên nhiên tại Ke Go Retreat.",
    )
    html = html.replace(
        "Luxury is found in details, both grand and subtle. Our curated facilities are designed to inspire balance and ease.",
        "Sự sang trọng ẩn trong từng chi tiết, dù nhỏ hay lớn. Các tiện nghi được tuyển chọn kỹ lưỡng để mang lại cảm giác cân bằng và thoải mái.",
    )
    html = html.replace(
        "Thức dậy cùng biển trời Hà Tĩnh and sunsets painted just for you, from the comfort of your private Thiên Cầm villa.",
        "Thức dậy cùng biển trời Hà Tĩnh và hoàng hôn được vẽ riêng cho bạn, trong sự thoải mái của villa riêng tư Thiên Cầm.",
    )
    # about-us/villas: English quote with mixed EN text
    html = html.replace(
        '"Mỗi góc Ke Go Retreat đều được chăm chút - beautiful yet effortless. Three nights here reminded me how to slow down and breathe again."',
        '"Mỗi góc Ke Go Retreat đều được chăm chút — đẹp mà không cầu kỳ. Ba đêm ở đây nhắc tôi cách chậm lại và thở."',
    )
    # dining.html: English body paragraphs
    html = html.replace(
        "Surrounded by lush gardens and ocean horizons, each dining space offers a setting that inspires connection and calm. From sunrise breakfasts to moonlit dinners, every moment is designed to linger.",
        "Bao quanh bởi vườn xanh và tầm nhìn ra đại dương, mỗi không gian ăn uống gợi lên cảm giác kết nối và bình yên. Từ bữa sáng lúc bình minh đến bữa tối dưới ánh trăng, mỗi khoảnh khắc đều đáng được thưởng thức thong thả.",
    )
    html = html.replace(
        "Ẩm thực is more than a meal — it is a journey. Heritage and global flavors, our chefs craft every dish with passion, precision, and artistry.",
        "Ẩm thực không chỉ là bữa ăn — đó là hành trình. Kết hợp hương vị địa phương và quốc tế, đầu bếp của chúng tôi tạo ra từng món với đam mê, tỉ mỉ và nghệ thuật.",
    )
    html = html.replace(
        "Khám phá các món tinh hoa trong thực đơn, carefully crafted to delight every palate.",
        "Khám phá các món tinh hoa trong thực đơn, được chắt lọc kỹ lưỡng để chiều lòng mọi khẩu vị.",
    )
    # dining.html: USD price → VND
    html = html.replace("$62.00", "450.000đ")
    html = html.replace("$62", "450.000đ")
    # villas-and-suites.html: USD pricing → VND (prices are in separate <div> from /night label)
    _villa_usd_map = {
        "$2,100": "15.500.000đ",
        "$1,650": "12.000.000đ",
        "$1,200": "8.700.000đ",
        "$730": "5.300.000đ",
        "$680": "5.000.000đ",
        "$575": "4.200.000đ",
        "$540": "3.900.000đ",
        "$420": "3.100.000đ",
    }
    for usd, vnd in _villa_usd_map.items():
        html = html.replace(f'>{usd}<', f'>{vnd}<')
    # /night label in price context → /đêm; "from" label → "từ"
    html = html.replace(
        'villa-price-text">/night</div>',
        'villa-price-text">/đêm</div>',
    )
    html = html.replace(
        'villa-price-text">from</div>',
        'villa-price-text">từ</div>',
    )
    # wellness.html: English body copy
    html = html.replace(
        "Spa & wellness is not an indulgence — it is a way of life. our holistic offerings are designed to restore balance, inspire clarity, and leave you renewed.",
        "Spa & chăm sóc sức khỏe không phải xa xỉ — đó là lối sống. Các liệu pháp toàn diện của chúng tôi được thiết kế để phục hồi cân bằng, khơi dậy sự sáng suốt và để bạn ra về tràn đầy năng lượng.",
    )
    html = html.replace(
        "We believe true wellbeing comes from harmony — of body, mind, and nature. Every treatment, ritual, and practice is crafted to reconnect you with yourself and the beauty around you.",
        "Chúng tôi tin rằng sức khỏe thật sự đến từ sự hài hòa — giữa cơ thể, tâm trí và thiên nhiên. Mọi liệu pháp, nghi thức và thực hành đều được thiết kế để kết nối lại bạn với bản thân và vẻ đẹp xung quanh.",
    )
    html = html.replace(
        "Each ritual is thoughtfully designed to restore balance, blending traditional techniques with contemporary luxury.",
        "Mỗi nghi thức được thiết kế tỉ mỉ để phục hồi cân bằng, kết hợp kỹ thuật truyền thống với sự sang trọng hiện đại.",
    )
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
    def cycle_attr(pool: list[str], pattern: str, attr: str) -> None:
        nonlocal html
        html = _travol_cycle(pool, pattern, html, attr)

    html = _travol_cycle(
        TRAVOL_DEST_IMGS,
        r'src="assets/duruthemes\.com/demo/html/travol/multipage-slider/img/destination/[^"]+\.jpg"',
        html,
    )
    cycle_attr(TRAVOL_DEST_IMGS, r'src="img/destination/[^"]+\.jpg"', "src")
    cycle_attr(TRAVOL_DEST_IMGS, r'data-background="img/destination/[^"]+\.jpg"', "data-background")
    html = _travol_cycle(
        TRAVOL_GALLERY_IMGS,
        r'src="assets/duruthemes\.com/demo/html/travol/multipage-slider/img/slider/[^"]+"',
        html,
    )
    cycle_attr(TRAVOL_GALLERY_IMGS, r'src="img/slider/[^"]+"', "src")
    cycle_attr(TRAVOL_GALLERY_IMGS, r'data-background="img/slider/[^"]+"', "data-background")
    html = _travol_cycle(
        TRAVOL_GALLERY_IMGS,
        r'href="assets/duruthemes\.com/demo/html/travol/multipage-slider/img/slider/[^"]+"',
        html,
        "href",
    )
    cycle_attr(TRAVOL_GALLERY_IMGS, r'href="img/slider/[^"]+"', "href")
    html = _travol_cycle(
        TRAVOL_BLOG_IMGS,
        r'src="assets/duruthemes\.com/demo/html/travol/multipage-slider/img/blog/[^"]+"',
        html,
    )
    cycle_attr(TRAVOL_BLOG_IMGS, r'src="img/blog/[^"]+"', "src")
    html = re.sub(
        r"url\(&quot;img/(?:slider|destination|blog)/[^&]+?\.(?:jpg|jpeg|png|webp)&quot;\)",
        lambda _m: f"url(&quot;{p(TRAVOL_GALLERY_IMGS[0])}&quot;)",
        html,
        flags=re.I,
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
    html = html.replace(">Gallery<", ">Thư viện<")
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


def fix_global_leftovers(html: str) -> str:
    for old, new in GLOBAL_LEFTOVERS:
        html = html.replace(old, new)
    route_repairs = (
        ("blog-posts_wellness-rituals-from-ha-tinh.html", "blog-posts_wellness-rituals-from-bali.html"),
        ("tours-categories_ha-tinh.html", "tours-categories_europe.html"),
        ("tours_thien-cam.html", "tours_spain.html"),
        ("tours_dong-loc.html", "tours_indonesia.html"),
        ("tours_huong-tich.html", "tours_egypt.html"),
        ("phòng.html", "rooms.html"),
    )
    for broken, target in route_repairs:
        html = html.replace(broken, target)
    return html


def process_html(fp: Path, html: str) -> str:
    slug = fp.relative_to(ROOT).parts[0]
    html = fix_crawl_artifacts(html)
    html = inject_head(html, GLOBAL_HIDE, "showcase-cleanup")
    html = strip_vendor(html)
    if slug == "colorlib-deluxe":
        html = fix_colorlib(html)
    elif slug == "moonlit-react":
        html = fix_moonlit(html)
    elif slug in ("wanderway-framer", "luxestay-framer", "mountain-lodge-framer"):
        if slug == "wanderway-framer":
            html = fix_wanderway(html)
            html = _apply_vi_list(html, FRAMER_VI)
            html = _apply_vi_list(html, FRAMER_VI_EXTRA)
        elif slug == "luxestay-framer":
            html = fix_luxestay(html)
            html = _apply_vi_list(html, FRAMER_VI)
            html = _apply_vi_list(html, FRAMER_VI_EXTRA)
            html = _apply_vi_list(html, LUXESTAY_VI)
            html = html.replace("contact@LuxeStay Ha Tinh.demo", "contact@luxestay.demo")
        else:
            html = fix_mountain(html)
            html = inject_head(html, MOUNTAIN_POLISH, "mountain-polish")
            html = _apply_vi_list(html, FRAMER_VI)
            html = _apply_vi_list(html, FRAMER_VI_EXTRA)
            html = _apply_vi_list(html, MOUNTAIN_VI)
            if fp.name == "index.html":
                html = inject_mountain_static_hero(html)
    elif slug == "hotale-resort":
        html = fix_hotale_uploads(html)
    elif slug == "asatha-luxury-webflow":
        html = fix_asatha_assets(html)
    elif slug == "travol-duruthemes":
        html = fix_travol_imgs(html)
    return fix_global_leftovers(html)


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
        if not slug.is_dir() or slug.name in ("assets", "docs", "tools"):
            continue
        for fp in slug.rglob("*.html"):
            html = fp.read_text(encoding="utf-8", errors="ignore")
            new = process_html(fp, html)
            if new != html:
                fp.write_text(new, encoding="utf-8")
                count += 1
        if slug.name == "moonlit-react":
            for fp in slug.rglob("*.js"):
                text = fp.read_text(encoding="utf-8", errors="ignore")
                new = fix_moonlit_text_asset(text)
                if new != text:
                    fp.write_text(new, encoding="utf-8")
                    count += 1
        if slug.name in ("wanderway-framer", "luxestay-framer", "mountain-lodge-framer"):
            for fp in list(slug.rglob("*.js")) + list(slug.rglob("*.mjs")):
                text = fp.read_text(encoding="utf-8", errors="ignore")
                new = fix_framer_text_asset(text)
                if new != text:
                    fp.write_text(new, encoding="utf-8")
                    count += 1
    symlink_luxestay_mjs()
    repaired = repair_placeholder_routes()
    print(f"fix_showcase: updated {count} html files")
    print(f"placeholder routes repaired: {repaired}")
    print("luxestay mjs symlinks created")


if __name__ == "__main__":
    main()
