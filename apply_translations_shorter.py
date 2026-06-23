import os

html_dir = r'c:\scratch\demo-ha-tinh-showcase\asatha-luxury-webflow'

replacements = {
    # Buttons / Links / CTAs
    '>Back to Home<': '>Trở về Trang chủ<',
    '>Back to home<': '>Trở về trang chủ<',
    '>Browse menu<': '>Xem thực đơn<',
    '>Get in touch<': '>Liên hệ<',
    '>Booking Enquiry<': '>Yêu cầu đặt phòng<',
    '>Event &amp; Celebration Booking<': '>Sự kiện &amp; Tiệc<', # Shorter
    '>Media &amp; Collaboration<': '>Hợp tác Truyền thông<', # Shorter
    '>General Inquiry<': '>Yêu cầu chung<',
    '>Find Us<': '>Tìm chúng tôi<',
    
    # Form fields
    '>Full Name*<': '>Họ và tên*<',
    '>Email*<': '>Email*<',
    '>Phone Number*<': '>Số điện thoại*<',
    '>Subject*<': '>Chủ đề*<',
    '>Select Bedroom*<': '>Chọn số phòng*<', # Shorter
    
    # Sections / Headings
    '>Gallery<': '>Thư viện ảnh<',
    '>Amenities<': '>Tiện ích<',
    '>Included Amenities<': '>Tiện ích có sẵn<', # Shorter
    '>What’s Included<': '>Dịch vụ bao gồm<',
    '>Room Availability<': '>Tình trạng phòng<',
    '>Help &amp; FAQs<': '>Hỗ trợ &amp; FAQs<',
    '>Terms &amp; Conditions<': '>Điều khoản chung<', # Shorter
    '>Experiences<': '>Trải nghiệm<',
    '>Activities<': '>Hoạt động<',
    '>Philosophy<': '>Triết lý<',
    '>Popular<': '>Phổ biến<',
    '>Rewards<': '>Ưu đãi<',
    '>Menus<': '>Thực đơn<',
    '>Resort<': '>Khu nghỉ dưỡng<',
    
    # Headings partials (often inside <em>)
    '<em>Experiences</em>': '<em>Trải nghiệm</em>',
    '<em>Gallery</em>': '<em>Thư viện ảnh</em>',
    '<em>Philosophy</em>': '<em>Triết lý</em>',
    '<em>retreats</em>': '<em>nghỉ dưỡng</em>',
    '<em>restore</em>': '<em>phục hồi</em>',
    
    # Amenities & Features
    '>High-speed WiFi<': '>WiFi tốc độ cao<',
    '>Air conditioning<': '>Điều hòa<', # Shorter
    '>Smart TV<': '>Smart TV<', # Keep English for short
    '>Private Pool<': '>Hồ bơi riêng<',
    '>Full Kitchen<': '>Bếp đầy đủ<',
    '>Butler Service<': '>Quản gia<',
    '>Garden view<': '>Hướng vườn<',
    '>Ocean view<': '>Hướng biển<',
    '>Indoor fireplace<': '>Lò sưởi<',
    '>Outdoor Entertainment<': '>Giải trí ngoài trời<',
    '>Fitness Studio<': '>Phòng Gym<', # Shorter
    '>Kitchen<': '>Nhà bếp<',
    '>Pets allowed<': '>Cho phép thú cưng<',
    '>Bath products<': '>Sản phẩm tắm gội<',
    '>Free parking on premises<': '>Bãi đậu xe miễn phí<',
    '>Seamless Check-In<': '>Nhận phòng nhanh<',
    '>Flexible Cancellation<': '>Hủy phòng linh hoạt<',
    
    # Booking details
    '>Check-in<': '>Nhận phòng<',
    '>Check-out<': '>Trả phòng<',
    '>Adults (Age 21+)<': '>Người lớn (21+)<',
    '>Children (Ages 2–12)<': '>Trẻ em (2–12 tuổi)<',
    '>/night<': ' / đêm<',
    '>Flexible cancellation policy available<': '>Chính sách hủy phòng linh hoạt<',
    '>Full refund available on cancellations made before 13 September.<': '>Hoàn tiền đầy đủ nếu hủy trước ngày 13 tháng 9.<',
    
    # FAQs
    '>Can I modify my booking after confirmation?<': '>Tôi có thể đổi lịch sau khi đặt không?<', # Shorter
    '>What payment methods are accepted?<': '>Hỗ trợ hình thức thanh toán nào?<', # Shorter
    
    # Packages / Wellness
    '>Daily breakfast<': '>Bữa sáng hàng ngày<',
    '>Welcome drink &amp; seasonal fruit basket on arrival<': '>Thức uống chào mừng &amp; trái cây theo mùa<',
    '>One-way airport transfer (up to 4 guests)<': '>Đưa đón sân bay 1 chiều (tối đa 4 khách)<',
    '>3 nights accommodation in a private villa<': '>3 đêm nghỉ tại villa riêng<',
    '>Package valid until 31 December 2025<': '>Gói có giá trị đến 31/12/2025<',
    
    # Spa terms
    '>Aroma<': '>Hương thơm<',
    '>Aromatherapy<': '>Trị liệu hương thơm<',
    '>Foot Reflexology<': '>Bấm huyệt bàn chân<',
    '>Full Body Stretch<': '>Kéo giãn toàn thân<',
    '>Couples Harmony<': '>Gắn kết đôi lứa<',
    '>Rejuvenation Journey<': '>Hành trình trẻ hóa<',
    '>Meditation<': '>Thiền định<',
    '>Holistic<': '>Toàn diện<',
    '>Yoga &amp;<': '>Yoga &amp;<',
    
    # Durations
    '<em>(30 min)</em>': '<em>(30p)</em>', # Shorter
    '<em>(45 min)</em>': '<em>(45p)</em>',
    '<em>(60 min)</em>': '<em>(60p)</em>',
    '<em>(2 hrs)</em>': '<em>(2h)</em>',
    '<em>(2.5 hrs)</em>': '<em>(2.5h)</em>',
    '<em>(3 hrs)</em>': '<em>(3h)</em>',
    
    # Reviews
    '>Guest Rating<': '>Đánh giá<', # Shorter
    '>Reviews Worldwide<': '>Đánh giá toàn cầu<',
    '12k+ Reviews': '12k+ Đánh giá',
    
    # Misc text
    '>Journey awaits<': '>Hành trình vẫy gọi<',
    '<em>Journey awaits</em>': '<em>Hành trình vẫy gọi</em>',
    '>Impressive<': '>Ấn tượng<',
    '>All<': '>Tất cả<',
    'villa &amp; resort': 'villa &amp; khu nghỉ dưỡng',
    'Villa &amp; Resort': 'Villa &amp; Khu nghỉ dưỡng',
    
    # Dates
    '>October 1, 2025<': '>1 Th10, 2025<',
    '>October 6, 2025<': '>6 Th10, 2025<',
    '>October 9, 2025<': '>9 Th10, 2025<',
    '>October 15, 2025<': '>15 Th10, 2025<',
    '>October 20, 2025<': '>20 Th10, 2025<',
    
    # Others
    '>Private Property<': '>Tài sản tư nhân<',
    'Aroma <em class="wood-700-text">': 'Hương thơm <em class="wood-700-text">',
    'Aromatherapy <em class="menu-food-name">(60 min)</em>': 'Trị liệu hương thơm <em class="menu-food-name">(60p)</em>',
    'Foot Reflexology <em class="menu-food-name">(45 min)</em>': 'Bấm huyệt bàn chân <em class="menu-food-name">(45p)</em>',
    'Full Body Stretch <em class="menu-food-name">(2 hrs)</em>': 'Kéo giãn toàn thân <em class="menu-food-name">(2h)</em>',
    'Couples Harmony <em class="menu-food-name">(2.5 hrs)</em>': 'Gắn kết đôi lứa <em class="menu-food-name">(2.5h)</em>',
    'Rejuvenation Journey <em class="menu-food-name">(3 hrs)</em>': 'Hành trình trẻ hóa <em class="menu-food-name">(3h)</em>',
    'Yoga &amp; <em class="wood-700-text">Meditation</em>': 'Yoga &amp; <em class="wood-700-text">Thiền định</em>',
    'Holistic <em class="wood-700-text">Chữa lành</em>': 'Chữa lành <em class="wood-700-text">toàn diện</em>',
    '>Menu<': '>Thực đơn<',
    'Menu <em class="wood-700-text">': 'Thực đơn <em class="wood-700-text">',
    '>Corporate Partnership<': '>Hợp tác doanh nghiệp<',
    '>Feedback or Complaint<': '>Góp ý &amp; Khiếu nại<',
    '>Reach<': '>Liên hệ<',
    '>Conditions<': '>Điều kiện<',
    '3 Bedrooms · Private Pool · Full Kitchen · Butler Service': '3 Phòng ngủ · Hồ bơi riêng · Bếp · Quản gia',
    'Experiences that': 'Trải nghiệm',
    'Experiences that restore': 'Trải nghiệm phục hồi',
    'Impressive <em class="wood-700-text">Gallery</em>': 'Thư viện ảnh <em class="wood-700-text">ấn tượng</em>',
    'Email*': 'Email*',
    '>P:<': '>Điện thoại:<',
    '>E:<': '>Email:<',
    '>Photography<': '>Nhiếp ảnh<',
    'Version 1.0': 'Phiên bản 1.0',
    '404 Page not found': '404 Trang không tìm thấy',
    '© KE GO RETREAT - VILLA &amp; RESORT.': '© KE GO RETREAT - VILLA &amp; RESORT.',
}

files_changed = 0

for filename in os.listdir(html_dir):
    if not filename.endswith('.html'):
        continue
    filepath = os.path.join(html_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = content
    for old_str, new_str in replacements.items():
        new_content = new_content.replace(old_str, new_str)

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        files_changed += 1

print(f"Applied translations to {files_changed} HTML files.")
