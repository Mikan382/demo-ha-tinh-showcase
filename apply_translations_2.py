import os

html_dir = r'c:\scratch\demo-ha-tinh-showcase\asatha-luxury-webflow'

replacements = {
    # Wellness & Spa specific strings with HTML tags
    'Aroma <em class="wood-700-text">': 'Hương thơm <em class="wood-700-text">',
    'Aromatherapy <em class="menu-food-name">(60 min)</em>': 'Trị liệu hương thơm <em class="menu-food-name">(60 phút)</em>',
    'Foot Reflexology <em class="menu-food-name">(45 min)</em>': 'Bấm huyệt bàn chân <em class="menu-food-name">(45 phút)</em>',
    'Full Body Stretch <em class="menu-food-name">(2 hrs)</em>': 'Kéo giãn toàn thân <em class="menu-food-name">(2 giờ)</em>',
    'Couples Harmony <em class="menu-food-name">(2.5 hrs)</em>': 'Gắn kết đôi lứa <em class="menu-food-name">(2.5 giờ)</em>',
    'Rejuvenation Journey <em class="menu-food-name">(3 hrs)</em>': 'Hành trình trẻ hóa <em class="menu-food-name">(3 giờ)</em>',
    'Yoga &amp; <em class="wood-700-text">Meditation</em>': 'Yoga &amp; <em class="wood-700-text">Thiền định</em>',
    'Holistic <em class="wood-700-text">Chữa lành</em>': 'Chữa lành <em class="wood-700-text">toàn diện</em>',
    
    # Dining leftovers
    'Nasi Campur <em class="menu-food-name">': 'Nasi Campur <em class="menu-food-name">', # Name of food, don't translate
    'Lava Chocolate <em class="menu-food-name">': 'Lava Chocolate <em class="menu-food-name">',
    
    # UI Elements
    '>Menu<': '>Thực đơn<',
    'Menu <em class="wood-700-text">': 'Thực đơn <em class="wood-700-text">',
    '>404 Page not found<': '>404 Không tìm thấy trang<',
    '>Corporate Partnership<': '>Hợp tác doanh nghiệp<',
    '>Feedback or Complaint<': '>Góp ý &amp; Khiếu nại<',
    '>Reach<': '>Liên hệ<',
    '>Popular<': '>Phổ biến<',
    '>Conditions<': '>Điều kiện<',
    '3 Bedrooms · Private Pool · Full Kitchen · Butler Service': '3 Phòng ngủ · Hồ bơi riêng · Bếp đầy đủ · Dịch vụ quản gia',
    
    # Hero/Text contexts
    'Experiences that': 'Những trải nghiệm',
    'Experiences that restore': 'Những trải nghiệm phục hồi',
    'Impressive <em class="wood-700-text">Gallery</em>': 'Thư viện ảnh <em class="wood-700-text">ấn tượng</em>',
    
    # Names / Styleguide specific
    '>Typography<': '>Kiểu chữ<',
    '>Iconography<': '>Biểu tượng<',
    '>Color Palette<': '>Bảng màu<',
    '>H1 Heading<': '>Tiêu đề H1<',
    '>H2 Heading<': '>Tiêu đề H2<',
    '>H3 Heading<': '>Tiêu đề H3<',
    '>H4 Heading<': '>Tiêu đề H4<',
    '>H5 Heading<': '>Tiêu đề H5<',
    '>H6 Heading<': '>Tiêu đề H6<',
    '>Large Paragraph<': '>Đoạn văn lớn<',
    '>Paragraph<': '>Đoạn văn<',
    '>Small Paragraph<': '>Đoạn văn nhỏ<',
    '>Large Text<': '>Chữ lớn<',
    '>Extra Large Text<': '>Chữ rất lớn<',
    '>Button<': '>Nút bấm<',
    '>Button Variant<': '>Biến thể nút bấm<',
    '>Button With Icon<': '>Nút bấm có biểu tượng<',
    '>White Button<': '>Nút bấm trắng<',
    '>Custom SVG Code<': '>Mã SVG tùy chỉnh<',
    '>License<': '>Bản quyền<',
    '>Styleguide<': '>Hướng dẫn phong cách<',
    
    # Misc and Form fields
    'Email*': 'Email*',
    '>P:<': '>Điện thoại:<',
    '>E:<': '>Email:<',
    
    # Some other files text
    '>Photography<': '>Nhiếp ảnh<',
    'All icons and logos used are from': 'Tất cả biểu tượng và logo được sử dụng từ',
    'This template includes custom SVG code.': 'Bản mẫu này bao gồm mã SVG tùy chỉnh.',
    '“All graphical assets in this template are licensed for personal and commercial use. If you\'d like to use a specific asset, please check the license below.”': '“Tất cả tài sản đồ họa trong bản mẫu này được cấp phép cho mục đích cá nhân và thương mại. Nếu bạn muốn sử dụng một tài sản cụ thể, vui lòng kiểm tra giấy phép bên dưới.”',
    'We used free personal and commercial use Urbanist &amp; Cardo licensed typography in this template. You can review the licenses and get the typeface for free if you want to use these.': 'Chúng tôi đã sử dụng kiểu chữ Urbanist &amp; Cardo miễn phí cho mục đích cá nhân và thương mại trong bản mẫu này. Bạn có thể xem xét giấy phép và tải bộ chữ miễn phí nếu muốn sử dụng chúng.',
    'This template\'s images and Videos are all free for both personal and commercial use. You can review the licensing and get free downloads of any image you choose to use on': 'Hình ảnh và Video của bản mẫu này đều miễn phí cho cả mục đích cá nhân và thương mại. Bạn có thể xem xét việc cấp phép và tải xuống miễn phí bất kỳ hình ảnh nào bạn chọn để sử dụng tại',
    'Initial Version Released. - Ke Go Retreat Luxury Template': 'Phiên bản đầu tiên được phát hành. - Bản mẫu sang trọng Ke Go Retreat',
    'Version 1.0': 'Phiên bản 1.0',
    '404 Page not found': '404 Trang không tìm thấy',
    '© KE GO RETREAT - VILLA &amp; RESORT.': '© KE GO RETREAT - VILLA &amp; RESORT.',
    
    # Check for (45 min) standalone
    '<em>(30 min)</em>': '<em>(30 phút)</em>',
    '<em>(45 min)</em>': '<em>(45 phút)</em>',
    '<em>(60 min)</em>': '<em>(60 phút)</em>',
    '<em>(2 hrs)</em>': '<em>(2 giờ)</em>',
    '<em>(2.5 hrs)</em>': '<em>(2.5 giờ)</em>',
    '<em>(3 hrs)</em>': '<em>(3 giờ)</em>',
    
    # And finally, just standard words
    '>Aroma<': '>Hương thơm<',
    '>Aromatherapy<': '>Trị liệu hương thơm<',
    '>Holistic<': '>Toàn diện<',
    '>Meditation<': '>Thiền định<',
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

print(f"Applied pass 2 translations to {files_changed} HTML files.")
