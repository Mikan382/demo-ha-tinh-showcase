import os

html_dir = r'c:\scratch\demo-ha-tinh-showcase\asatha-luxury-webflow'

# Dictionary of literal replacements (from most specific/longest to shortest to prevent partial matches)
replacements = {
    # Buttons / Links / CTAs
    '>Back to Home<': '>Trở về Trang chủ<',
    '>Back to home<': '>Trở về trang chủ<',
    '>Browse menu<': '>Xem thực đơn<',
    '>Get in touch<': '>Liên hệ<',
    '>Booking Enquiry<': '>Yêu cầu đặt phòng<',
    '>Event &amp; Celebration Booking<': '>Đặt tiệc &amp; Sự kiện<',
    '>Media &amp; Collaboration<': '>Truyền thông &amp; Hợp tác<',
    '>General Inquiry<': '>Yêu cầu chung<',
    '>Find Us<': '>Tìm chúng tôi<',
    
    # Form fields
    '>Full Name*<': '>Họ và tên*<',
    '>Email*<': '>Email*<',
    '>Phone Number*<': '>Số điện thoại*<',
    '>Subject*<': '>Chủ đề*<',
    '>Select Bedroom*<': '>Chọn số phòng ngủ*<',
    
    # Sections / Headings
    '>Gallery<': '>Thư viện ảnh<',
    '>Amenities<': '>Tiện ích<',
    '>Included Amenities<': '>Tiện ích bao gồm<',
    '>What’s Included<': '>Các dịch vụ bao gồm<',
    '>Room Availability<': '>Tình trạng phòng<',
    '>Help &amp; FAQs<': '>Hỗ trợ &amp; Câu hỏi thường gặp<',
    '>Terms &amp; Conditions<': '>Điều khoản &amp; Điều kiện<',
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
    '>Air conditioning<': '>Điều hòa không khí<',
    '>Smart TV<': '>TV Thông minh<',
    '>Private Pool<': '>Hồ bơi riêng<',
    '>Full Kitchen<': '>Bếp đầy đủ tiện nghi<',
    '>Butler Service<': '>Dịch vụ quản gia<',
    '>Garden view<': '>Hướng vườn<',
    '>Ocean view<': '>Hướng biển<',
    '>Indoor fireplace<': '>Lò sưởi trong nhà<',
    '>Outdoor Entertainment<': '>Khu giải trí ngoài trời<',
    '>Fitness Studio<': '>Phòng tập thể hình<',
    '>Kitchen<': '>Nhà bếp<',
    '>Pets allowed<': '>Cho phép thú cưng<',
    '>Bath products<': '>Sản phẩm tắm gội<',
    '>Free parking on premises<': '>Bãi đậu xe miễn phí<',
    '>Seamless Check-In<': '>Nhận phòng nhanh chóng<',
    '>Flexible Cancellation<': '>Hủy phòng linh hoạt<',
    
    # Booking details
    '>Check-in<': '>Nhận phòng<',
    '>Check-out<': '>Trả phòng<',
    '>Adults (Age 21+)<': '>Người lớn (Từ 21 tuổi)<',
    '>Children (Ages 2–12)<': '>Trẻ em (2–12 tuổi)<',
    '>/night<': ' / đêm<',
    '>Flexible cancellation policy available<': '>Chính sách hủy phòng linh hoạt<',
    '>Full refund available on cancellations made before 13 September.<': '>Hoàn tiền đầy đủ cho các yêu cầu hủy trước ngày 13 tháng 9.<',
    
    # FAQs
    '>Can I modify my booking after confirmation?<': '>Tôi có thể thay đổi đặt phòng sau khi đã xác nhận không?<',
    '>What payment methods are accepted?<': '>Phương thức thanh toán nào được chấp nhận?<',
    
    # Packages / Wellness
    '>Daily breakfast<': '>Bữa sáng hàng ngày<',
    '>Welcome drink &amp; seasonal fruit basket on arrival<': '>Thức uống chào mừng &amp; giỏ trái cây theo mùa khi đến<',
    '>One-way airport transfer (up to 4 guests)<': '>Đưa đón sân bay một chiều (tối đa 4 khách)<',
    '>3 nights accommodation in a private villa<': '>3 đêm nghỉ tại villa riêng<',
    '>Package valid until 31 December 2025<': '>Gói ưu đãi có giá trị đến 31/12/2025<',
    
    # Spa terms
    '>Aroma<': '>Hương thơm<',
    '>Aromatherapy<': '>Trị liệu hương thơm<',
    '>Foot Reflexology<': '>Ấn huyệt bàn chân<',
    '>Full Body Stretch<': '>Kéo giãn toàn thân<',
    '>Couples Harmony<': '>Gắn kết đôi lứa<',
    '>Rejuvenation Journey<': '>Hành trình trẻ hóa<',
    '>Meditation<': '>Thiền định<',
    '>Holistic<': '>Toàn diện<',
    '>Yoga &amp;<': '>Yoga &amp;<', # Need to translate the surrounding text ideally, but let's do safe replacements
    
    # Durations
    '<em>(30 min)</em>': '<em>(30 phút)</em>',
    '<em>(45 min)</em>': '<em>(45 phút)</em>',
    '<em>(60 min)</em>': '<em>(60 phút)</em>',
    '<em>(2 hrs)</em>': '<em>(2 giờ)</em>',
    '<em>(2.5 hrs)</em>': '<em>(2.5 giờ)</em>',
    '<em>(3 hrs)</em>': '<em>(3 giờ)</em>',
    
    # Reviews
    '>Guest Rating<': '>Đánh giá của khách<',
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
    '>October 1, 2025<': '>1 Tháng 10, 2025<',
    '>October 6, 2025<': '>6 Tháng 10, 2025<',
    '>October 9, 2025<': '>9 Tháng 10, 2025<',
    '>October 15, 2025<': '>15 Tháng 10, 2025<',
    '>October 20, 2025<': '>20 Tháng 10, 2025<',
    
    # Others
    '>Private Property<': '>Tài sản tư nhân<',
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
        
    # Some special fixes for attributes
    new_content = new_content.replace('placeholder="Full Name*"', 'placeholder="Họ và tên*"')
    new_content = new_content.replace('placeholder="Email*"', 'placeholder="Email*"')
    new_content = new_content.replace('placeholder="Phone Number*"', 'placeholder="Số điện thoại*"')
    new_content = new_content.replace('placeholder="Subject*"', 'placeholder="Chủ đề*"')
    
    # Edge case phrases that might not have >< tight wrappers
    new_content = new_content.replace('2 Bedroom Ocean View Villa', 'Villa 2 Phòng ngủ Hướng biển')
    new_content = new_content.replace('5+ Bedroom', '5+ Phòng ngủ')
    new_content = new_content.replace('3 Bedrooms &middot; Private Pool &middot; Full Kitchen &middot; Butler Service', '3 Phòng ngủ &middot; Hồ bơi riêng &middot; Bếp &middot; Dịch vụ quản gia')
    new_content = new_content.replace('Hosted by', 'Chủ nhà:')
    new_content = new_content.replace('2 years hosting', '2 năm làm chủ nhà')

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        files_changed += 1

print(f"Applied translations to {files_changed} HTML files.")
