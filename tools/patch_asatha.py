"""One-time patch to fix fix_showcase.py: review keys, FROM labels, new replacements."""
import re

PATH = __file__.replace("patch_asatha.py", "fix_showcase.py")
with open(PATH, encoding="utf-8") as f:
    src = f.read()

changes = []

def replace_once(old, new, label=""):
    global src
    if old in src:
        src = src.replace(old, new, 1)
        changes.append(f"OK: {label or old[:60]}")
    else:
        changes.append(f"MISS: {label or old[:60]}")

# ─── Fix 4 remaining review keys ──────────────────────────────────────────────
# These keys currently use ASCII " and ASCII ' (via \' escape in single-quoted string)
# but HTML has U+201C, U+2019, U+201D.  Replace with Python \uXXXX escapes.

replace_once(
    '''        '"The quiet wasn\\'t silence, it was music. Waking up to soft light and sleeping under stars made this trip unforgettable."',''',
    '''        "\\u201cThe quiet wasn\\u2019t silence, it was music. Waking up to soft light and sleeping under stars made this trip unforgettable.\\u201d",''',
    "review: The quiet wasn't",
)

replace_once(
    '''        '"I\\'ve traveled often, but never felt this cared for. The staff remembered my name, my tea, even my favorite view."',''',
    '''        "\\u201cI\\u2019ve traveled often, but never felt this cared for. The staff remembered my name, my tea, even my favorite view.\\u201d",''',
    "review: I've traveled",
)

replace_once(
    '''        '"Ke Go Retreat felt like a pause from life, but one that gave me more energy than before. I left lighter, calmer, and deeply inspired."',''',
    '''        "\\u201cKe Go Retreat felt like a pause from life, but one that gave me more energy than before. I left lighter, calmer, and deeply inspired.\\u201d",''',
    "review: Ke Go Retreat felt like",
)

replace_once(
    '''        '"It was more than a resort—it felt like home, but more peaceful, more beautiful, more complete."',''',
    '''        "\\u201cIt was more than a resort\\u2014it felt like home, but more peaceful, more beautiful, more complete.\\u201d",''',
    "review: It was more than",
)

# ─── Fix Tĩnh's apostrophe ────────────────────────────────────────────────────
replace_once(
    "        \"Journey into Hà Tĩnh's heart with visits to temples, waterfalls, and hidden beaches. Authentic cultural encounters paired with luxury comfort create a memorable escape.\",",
    "        \"Journey into Hà Tĩnh\\u2019s heart with visits to temples, waterfalls, and hidden beaches. Authentic cultural encounters paired with luxury comfort create a memorable escape.\",",
    "Tĩnh's heart",
)

# ─── Fix FROM labels (ALLCAPS → mixed case matching HTML) ─────────────────────
replace_once(
    '    html = html.replace("FROM UK · STAYED IN OCEAN SUITE", "Từ Anh Quốc · Nghỉ tại Ocean Suite")',
    '    html = html.replace("FROM UK · Stayed in Ocean Suite", "Từ Anh Quốc · Nghỉ tại Ocean Suite")',
    "FROM UK label",
)
replace_once(
    '    html = html.replace("FROM INDIA · STAYED IN VILLA VƯỚN XANH", "Từ Ấn Độ · Nghỉ tại Villa VƯờn Xanh")',
    '    html = html.replace("FROM India · Stayed in Villa VƯờn Xanh", "Từ Ấn Độ · Nghỉ tại Villa VƯờn Xanh")',
    "FROM India label",
)
replace_once(
    '    html = html.replace("FROM HÀ TĨNH · STAYED IN HORIZON PAVILION", "Từ Hà Tĩnh · Nghỉ tại Horizon Pavilion")',
    '    html = html.replace("FROM Hà Tĩnh · Stayed in Horizon Pavilion", "Từ Hà Tĩnh · Nghỉ tại Horizon Pavilion")',
    "FROM Hà Tĩnh label",
)
replace_once(
    '    html = html.replace("FROM GERMANY · STAYED IN SUITE AN YÊN", "Từ Đức · Nghỉ tại Suite An Yên")',
    '    html = html.replace("FROM Germany · Stayed in Suite An Yên", "Từ Đức · Nghỉ tại Suite An Yên")',
    "FROM Germany label",
)
replace_once(
    '    html = html.replace("FROM JAPAN · STAYED IN THE RESIDENCE", "Từ Nhật Bản · Nghỉ tại The Residence")',
    '    html = html.replace("FROM Japan · Stayed in The Residence", "Từ Nhật Bản · Nghỉ tại The Residence")',
    "FROM Japan label",
)

# ─── Add new replacements before the vendor-hide check ───────────────────────
NEW_REPLACEMENTS = '''    # Booking CTA
    html = html.replace("Or booking with partners", "Hoặc đặt qua đối tác")
    # Form messages
    html = html.replace("Thank you! Your submission has been received!", "Cảm ơn! Chúng tôi đã nhận được thông tin của bạn.")
    html = html.replace("Oops! Something went wrong while submitting the form.", "Đã xảy ra lỗi khi gửi biểu mẫu.")
    html = html.replace('data-wait="Please wait..."', 'data-wait="Vui lòng chờ..."')
    # About vision sentence (mixed EN prefix)
    html = html.replace(
        "Ke Go Retreat was created with one vision:",
        "Ke Go Retreat được tạo ra với một tầm nhìn:",
    )
    # Footer contact
    html = html.replace("+62 812 3456 7890", "+84 239 385 6789")
    html = html.replace("stay@asatha.com", "stay@kego.demo")
    html = html.replace("Reception: ", "Lễ tân: ")
    # Address: remove cruft
    html = html.replace(
        "123 Khu vực Thiên Cầm No. 88, Thiên Cầm, Hà Tĩnh, Hà Tĩnh 80361, Đồng Lộc",
        "Thiên Cầm, Hà Tĩnh",
    )
    # "Made by" footer credit
    html = html.replace(">Made by</div>", ">Bản demo</div>")
    # Form options — bedroom
    html = html.replace(">1 Bedroom<", ">1 Phòng ngủ<")
    html = html.replace(">2 Bedroom<", ">2 Phòng ngủ<")
    html = html.replace(">3 Bedroom<", ">3 Phòng ngủ<")
    html = html.replace(">4 Bedroom<", ">4 Phòng ngủ<")
    # Form options — adults
    html = html.replace(">2 Adults<", ">2 người lớn<")
    html = html.replace(">3 Adults<", ">3 người lớn<")
    html = html.replace(">4 Adults<", ">4 người lớn<")
    html = html.replace(">5 Adults<", ">5 người lớn<")
    html = html.replace(">5+ Adults<", ">5+ người lớn<")
    # Form options — children
    html = html.replace(">1 Child<", ">1 trẻ em<")
    html = html.replace(">2 Child<", ">2 trẻ em<")
    html = html.replace(">3 Child<", ">3 trẻ em<")
    html = html.replace(">3+ Child<", ">3+ trẻ em<")
    # Showcase nav modal items still in English
    html = html.replace(">Villas Details<", ">Chi tiết villa<")
    html = html.replace(">Package Details<", ">Chi tiết gói<")
    html = html.replace(">Blogs lists<", ">Danh sách blog<")
    html = html.replace(">Blog Article<", ">Bài viết<")
    html = html.replace(">Liên hệ us<", ">Liên hệ<")
    html = html.replace(">404 Page<", ">Trang 404<")

    # --- Comprehensive translations added in audit ---
    # Common text
    html = html.replace(">Villa & Suites<", ">Biệt thự & Phòng<")
    html = html.replace(">Spa & wellness<", ">Spa & Chăm sóc sức khỏe<")
    html = html.replace(">Spa & wellness Escape<", ">Gói Wellness Escape<")
    html = html.replace(">Utility<", ">Tiện ích<")
    html = html.replace(">Villas Details<", ">Chi tiết biệt thự<")
    html = html.replace(">Liên hệ Us<", ">Liên hệ<")
    html = html.replace(">Liên hệ us<", ">Liên hệ<")
    html = html.replace("© KE GO RETREAT - VILLA AND RESORT.", "© KE GO RETREAT - VILLA & RESORT.")
    html = html.replace(">starting from<", ">chỉ từ<")
    html = html.replace(">starting from", ">chỉ từ")
    html = html.replace("starting from<", "chỉ từ<")
    html = html.replace(">from<", ">từ<")
    html = html.replace("/for 3 night", "/3 đêm")
    html = html.replace("/for 5 night", "/5 đêm")
    html = html.replace("Read Khác", "Đọc thêm")

    # 404 Page
    html = html.replace("Not Found - Ke Go Retreat Luxury - HTML website template", "Không tìm thấy trang — Ke Go Retreat Hà Tĩnh")
    html = html.replace("The page you are looking for is", "Trang bạn đang tìm kiếm")
    html = html.replace("The page you’re looking for has taken a detour. Let’s get you back to exploring.", "Trang bạn tìm kiếm không tồn tại hoặc đã được di chuyển. Hãy quay lại trang chủ.")

    # About-us page
    html = html.replace("Villas and Resorts Worldwide", "Khu nghỉ dưỡng cao cấp")
    html = html.replace("“We wanted Ke Go Retreat to feel less like a destination and more like a return to what matters most.”", "“Chúng tôi muốn Ke Go Retreat không chỉ là một điểm đến, mà là hành trình trở về với những gì ý nghĩa nhất.”")

    # Blog common and blog-posts
    html = html.replace("A Journey into tranquility - the essence of asatha - Ke Go Retreat Luxury - HTML website template", "Hành trình vào sự tĩnh lặng — Tinh hoa Ke Go Retreat Hà Tĩnh")
    html = html.replace("A Journey into tranquility - the essence of asatha", "Hành trình vào sự tĩnh lặng — Tinh hoa Ke Go Retreat")
    html = html.replace("Step inside our sanctuary at Thiên Cầm, where nature and design meet to create an effortless sense of calm. Discover what makes Ke Go Retreat more than just a stay.", "Bước vào không gian thanh tịnh tại Thiên Cầm, nơi thiên nhiên và thiết kế giao thoa tạo nên cảm giác bình yên tự nhiên. Khám phá điều làm Ke Go Retreat trở nên đặc biệt.")
    html = html.replace("Perched high on the cliffs of Thiên Cầm, Ke Go Retreat is more than a resort — it is a sanctuary. Here, the rhythm of the ocean sets the pace of life, and every corner is designed to bring you closer to balance, beauty, and serenity. Step inside our world, where nature and design exist in perfect harmony, and discover why Ke Go Retreat is not just a stay, but a journey into tranquility.", "Tọa lạc trên đồi cao hướng ra biển Thiên Cầm, Ke Go Retreat không chỉ là một khu nghỉ dưỡng — đó là một chốn bình yên. Tại đây, tiếng sóng biển nhịp nhàng dẫn lối cho cuộc sống, và mọi góc nhỏ đều được thiết kế để mang lại sự cân bằng, vẻ đẹp và sự thanh tịnh. Hãy bước vào thế giới của chúng tôi, nơi thiên nhiên và kiến trúc hòa quyện hoàn hảo.")
    html = html.replace("Where nature meets design", "Nơi thiên nhiên giao hòa cùng kiến trúc")
    html = html.replace("From the moment you arrive, the natural landscape of Thiên Cầm surrounds you — sweeping ocean vistas, lush tropical greenery, and skies painted with Hà Tĩnh’s legendary sunsets. Every villa and suite at Ke Go Retreat is shaped with these elements in mind, blending clean architectural lines with organic textures. The result is a seamless union of sophistication and soul, where luxury feels effortless.", "Ngay từ khoảnh khắc đặt chân đến, cảnh quan tự nhiên của Thiên Cầm sẽ ôm trọn lấy bạn — tầm nhìn đại dương bao la, những rặng cây nhiệt đới xanh mướt và bầu trời được dệt nên bởi hoàng hôn huyền thoại của Hà Tĩnh. Mỗi căn villa và suite tại Ke Go Retreat đều được tạo tác từ những chất liệu tự nhiên đó, kết hợp giữa các đường nét kiến trúc tinh tế với chất liệu hữu cơ.")
    html = html.replace("Tranquility at Ke Go Retreat is not an accident; it’s carefully crafted. Each space is designed to slow you down — soft light filters through open courtyards, natural stone pathways lead to hidden gardens, and gentle breezes carry the scent of frangipani across private terraces. Every detail, from bespoke interiors to hand-selected art pieces, contributes to an atmosphere where time feels suspended.", "Sự tĩnh lặng tại Ke Go Retreat không phải là ngẫu nhiên, mà được tạo tác một cách tỉ mỉ. Mỗi không gian được thiết kế để bạn sống chậm lại — ánh sáng dịu nhẹ qua những khoảng sân mở, những lối đi lát đá tự nhiên dẫn đến các khu vườn ẩn mình, và làn gió nhẹ mang hương hoa đại mát lành qua những ban công riêng tư.")
    html = html.replace("“Here, silence is not empty — it is full of presence, balance, and beauty.”", "“Tại đây, sự im lặng không hề trống rỗng — nó đong đầy sự hiện diện, cân bằng và vẻ đẹp.”")
    html = html.replace("Life at Ke Go Retreat extends beyond the villa walls. Begin your day with sunrise yoga overlooking the cliffs, surrender to the healing touch of traditional Hà Tĩnhnese massages at our wellness center, or savor a chef’s tasting menu that celebrates local ingredients. For the adventurous, guided explorations of Thiên Cầm’s temples, hidden beaches, and surf breaks offer a deeper connection to this land’s spiritual and cultural richness.", "Cuộc sống tại Ke Go Retreat mở rộng ra ngoài những bức tường villa. Bắt đầu ngày mới với bài tập yoga đón bình minh trên đồi hướng biển, thả mình vào liệu pháp massage truyền thống Hà Tĩnh tại trung tâm wellness, hay thưởng thức thực đơn đặc biệt tôn vinh nguyên liệu địa phương từ bếp trưởng.")
    html = html.replace("At the heart of Ke Go Retreat is the promise of restoration. Guests often leave with more than memories — they carry home a sense of calm, clarity, and connection. Whether you come seeking solitude, romance, or inspiration, Ke Go Retreat is designed to be the place you return to within yourself, long after you’ve departed.", "Cốt lõi của Ke Go Retreat là lời hứa về sự phục hồi. Du khách rời đi không chỉ mang theo những kỷ niệm — họ mang về sự an nhiên, sáng suốt và kết nối nội tâm.")
    html = html.replace("Embrace the essence", "Cảm nhận tinh hoa")
    html = html.replace("At Ke Go Retreat, tranquility isn’t just found — it’s felt. It’s in the stillness of dawn by the infinity pool, the laughter shared over dinner beneath the stars, and the silence that holds you when the world falls away. This is the essence of Ke Go Retreat. This is where serenity awaits.", "Tại Ke Go Retreat, sự tĩnh lặng không chỉ được tìm thấy — mà được cảm nhận sâu sắc. Đó là sự tĩnh lặng của bình minh bên hồ bơi vô cực, tiếng cười rộn rã trong bữa tối dưới trời sao, và khoảng lặng ôm lấy bạn khi thế giới ồn ào lùi xa. Đó chính là tinh túy của Ke Go Retreat.")

    # Other blogs
    html = html.replace("Culinary notes from our chef - Ke Go Retreat Luxury - HTML website template", "Ghi chú ẩm thực từ bếp trưởng — Ke Go Retreat")
    html = html.replace("Culinary notes from our chef", "Ghi chú ẩm thực từ bếp trưởng")
    html = html.replace("Chef Malee shares insights into curating authentic Thai flavors with a modern, refined touch.", "Đầu bếp chia sẻ nghệ thuật chắt lọc hương vị ẩm thực địa phương với nét tinh tế hiện đại.")
    html = html.replace("Designing with nature - Ke Go Retreat Luxury - HTML website template", "Thiết kế hòa quyện thiên nhiên — Ke Go Retreat")
    html = html.replace("Designing with nature", "Thiết kế hòa quyện thiên nhiên")
    html = html.replace("Sustainable luxury - Ke Go Retreat Luxury - HTML website template", "Sự sang trọng bền vững — Ke Go Retreat")
    html = html.replace("Sustainable luxury", "Sự sang trọng bền vững")
    html = html.replace("Our commitment to respecting people and nature, while delivering unmatched hospitality.", "Cam kết của chúng tôi trong việc tôn trọng con người và thiên nhiên, đồng thời mang đến dịch vụ hiếu khách vô song.")
    html = html.replace("Spa & wellness rituals from ha-tinh - Ke Go Retreat Luxury - HTML website template", "Nghi thức Spa & Chăm sóc sức khỏe từ Hà Tĩnh — Ke Go Retreat")
    html = html.replace("Spa & wellness rituals from ha-tinh", "Nghi thức Spa & Chăm sóc sức khỏe từ Hà Tĩnh")
    html = html.replace("Explore ancient healing practices that inspire our spa therapies, designed to restore balance and inner peace.", "Khám phá các liệu pháp chữa lành cổ xưa truyền cảm hứng cho dịch vụ spa của chúng tôi, giúp phục hồi sự cân bằng và bình yên nội tâm.")

    # Blog page
    html = html.replace("Latest <em>News</em>", "Tin tức <em>mới nhất</em>")
    html = html.replace("Recent <em>Stories</em>", "Bài viết <em>gần đây</em>")
    html = html.replace("Latest", "Mới nhất")
    html = html.replace("News", "Tin tức")
    html = html.replace("Recent", "Gần đây")
    html = html.replace("Stories", "Bài viết")

    # Contact-us page
    html = html.replace("Fill out the form below and let us help you plan your perfect getaway.", "Điền vào biểu mẫu bên dưới và để chúng tôi giúp bạn lên kế hoạch cho kỳ nghỉ hoàn hảo.")
    html = html.replace("Spa & Spa & wellness Appointment", "Đặt lịch Spa & Chăm sóc sức khỏe")
    html = html.replace("Spa &amp; Spa &amp; wellness Appointment", "Đặt lịch Spa & Chăm sóc sức khỏe")
    html = html.replace("I agree with the", "Tôi đồng ý với")
    html = html.replace("How can I book my stay at Ke Go Retreat?", "Làm thế nào để tôi đặt phòng tại Ke Go Retreat?")
    html = html.replace("You can book directly on our website using the Book Now button, or contact our reservations team via email or WhatsApp for personalized assistance.", "Bạn có thể đặt trực tiếp trên website bằng cách bấm nút Đặt phòng, hoặc liên hệ đội ngũ hỗ trợ qua email hoặc Zalo/WhatsApp để được tư vấn riêng.")
    html = html.replace("We accept all major credit cards, international debit cards, and secure bank transfers. For on-site payments, we also accept digital wallets.", "Chúng tôi chấp nhận thẻ tín dụng, thẻ ghi nợ quốc tế và chuyển khoản ngân hàng an toàn. Khi thanh toán tại chỗ, chúng tôi cũng hỗ trợ các ví điện tử thông dụng.")
    html = html.replace("Yes, bookings can be modified up to 7 days before your arrival date, subject to availability and any applicable rate changes.", "Có, thông tin đặt phòng có thể thay đổi tối đa 7 ngày trước ngày nhận phòng, tùy thuộc vào tình trạng phòng trống và áp dụng thay đổi giá nếu có.")
    html = html.replace("What is the cancellation policy at Ke Go Retreat?", "Chính sách hủy phòng tại Ke Go Retreat là gì?")
    html = html.replace("Cancellations made 14 days prior to arrival are free of charge. Cancellations within 14 days may incur one night’s stay as a fee. No-shows will be charged the full amount.", "Hủy phòng trước 14 ngày so với ngày nhận phòng sẽ được miễn phí. Hủy phòng trong vòng 14 ngày có thể chịu phí tương đương một đêm nghỉ. Trường hợp không đến nhận phòng sẽ tính phí toàn bộ thời gian đặt.")
    html = html.replace("Do you offer seasonal promotions or packages?", "Retreat có các gói ưu đãi hoặc khuyến mại theo mùa không?")
    html = html.replace("Yes, we offer exclusive seasonal deals, wellness packages, and honeymoon specials throughout the year.", "Có, chúng tôi có các gói ưu đãi đặc biệt theo mùa, gói chăm sóc sức khỏe và ưu đãi tuần trăng mật xuyên suốt cả năm.")

    # Dining page
    html = html.replace("A culinary", "Hành trình ẩm thực")
    html = html.replace('"Each dish carries the essence of our land and culture, blending tradition with innovation to create something truly unforgettable."', '“Mỗi món ăn đều mang tinh hoa của vùng đất và văn hóa bản địa, kết hợp truyền thống và hiện đại để tạo nên trải nghiệm khó quên.”')
    html = html.replace("Chef Aruna – Executive Chef", "Bếp trưởng Aruna")
    html = html.replace("Culinary", "Ẩm thực")
    html = html.replace("Browse our", "Khám phá")
    html = html.replace("Slow-roasted tomatoes, ginger, and coconut cream", "Cà chua nướng chậm, gừng và kem dừa")
    html = html.replace("with Tamarind Glaze", "sốt me chua ngọt")
    html = html.replace("Fragrant jasmine rice and seasonal greens", "Cơm lài thơm và rau xanh theo mùa")

    # Index page
    html = html.replace("From serene suites to curated experiences, Ke Go Retreat is more than a resort—it’s a retreat for the soul. Here, every detail is thoughtfully designed to celebrate the art of living beautifully.", "Từ các căn suite yên bình đến trải nghiệm được chọn lọc kỹ lưỡng, Ke Go Retreat không chỉ là khu nghỉ dưỡng — đó là nơi vỗ về tâm hồn. Ở đây, mọi chi tiết đều được thiết kế để tôn vinh nghệ thuật sống đẹp.")
    html = html.replace("Your benefits don’t end at check-out. Use or transfer points anytime with our select partners, or shop your favorite brands while staying connected to the Ke Go Retreat lifestyle.", "Đặc quyền thành viên không kết thúc khi trả phòng. Tích lũy và đổi điểm bất cứ lúc nào với các đối tác liên kết hoặc mua sắm các thương hiệu yêu thích.")
    html = html.replace("About our", "Về khu")
    html = html.replace("villas and resort", "villa & resort")

    # Packages & Popular Packages pages
    html = html.replace("Celebrate togetherness in the most romantic way. Private villa adorned with flower petals, couples’ spa rituals, and a four-course candlelit dinner under the stars.", "Tôn vinh sự gắn kết theo cách lãng mạn nhất. Biệt thự riêng tư rải đầy cánh hồng ngọt ngào, nghi thức spa dành cho đôi lứa và bữa tối lung linh dưới ánh nến dưới trời sao.")
    html = html.replace("Back to packages", "Quay lại danh sách gói")
    html = html.replace("Arrive at your convenience with our self check-in service, assisted by dedicated villa staff.", "Nhận phòng tự động dễ dàng với sự hỗ trợ từ nhân sự biệt thự chuyên nghiệp.")
    html = html.replace("Daily breakfast for 2 adults + 2 children", "Ăn sáng hàng ngày cho 2 người lớn + 2 trẻ em")
    html = html.replace("2 x signature massages for parents", "2 liệu trình massage đặc trưng dành cho bố mẹ")
    html = html.replace("Complimentary pool floaties & toys for kids", "Miễn phí phao bơi và đồ chơi dưới nước cho trẻ")
    html = html.replace("Free kids’ meals (lunch & dinner when dining with parents)", "Miễn phí bữa ăn cho trẻ em (trưa & tối khi dùng bữa cùng bố mẹ)")
    html = html.replace("1 x babysitter for 4 hours", "Dịch vụ trông trẻ miễn phí trong 4 giờ (1 lần)")
    html = html.replace("Subject to villa availability at the time of booking", "Áp dụng tùy thuộc vào tình trạng biệt thự trống tại thời điểm đặt")
    html = html.replace("For extended stays or 2026 bookings,", "Để lưu trú dài ngày hoặc đặt phòng năm 2026,")
    html = html.replace("please contact:", "vui lòng liên hệ:")

    # Villas & Suites details pages
    html = html.replace("Dive into adventure with a luxury vessel built for snorkeling and diving excursions. Includes professional guides, gourmet dining, and spacious lounges.", "Hành trình khám phá biển khơi với du thuyền cao cấp trang bị cho hoạt động lặn biển. Đã bao gồm hướng dẫn viên, ẩm thực tinh tế và không gian thư giãn rộng rãi.")
    html = html.replace("Back to Villa & Suites", "Quay lại danh sách biệt thự & phòng")
    html = html.replace("Hosted by Nature Sweet Homes", "Quản lý bởi Ke Go Retreat")
    html = html.replace("Enjoy evenings by the firepit, alfresco dining, and a private BBQ area — perfect for relaxed summer gatherings.", "Tận hưởng những buổi tối ấm áp bên bếp lửa ngoài trời, ăn uống alfresco và khu vực nướng BBQ riêng — lý tưởng cho những buổi tụ họp ấm cúng.")
    html = html.replace("Outdoor Shower · Private Courtyard · In-room Dining", "Vòi sen ngoài trời · Sân vườn riêng · Phục vụ ẩm thực tại phòng")
    html = html.replace("Residence Pavilion is more than just a private villa — it’s a retreat designed for those who value space, privacy, and effortless sophistication. Blending timeless architecture with natural surroundings, this residence offers sweeping views, refined interiors, and the feeling of a secluded sanctuary.", "Residence Pavilion không chỉ là một biệt thự riêng tư — đó là không gian nghỉ dưỡng được thiết kế cho những ai trân quý không gian rộng mở, sự riêng tư và nét tinh tế tự nhiên. Kết hợp kiến trúc vượt thời gian và cảnh quan xung quanh, dinh thự này mở ra tầm nhìn bao la, nội thất sang trọng và cảm giác bình yên của một ốc đảo biệt lập.")
    html = html.replace("Step inside and you’ll discover airy living spaces adorned with elegant furnishings, floor-to-ceiling windows that invite the outdoors in, and a seamless flow between modern design and tropical tranquility. Every corner of this residence has been thoughtfully curated to elevate your stay into an unforgettable experience.", "Bước vào bên trong, bạn sẽ cảm nhận được không gian sống thoáng đãng được bài trí nội thất thanh nhã, những ô cửa kính kịch trần đón trọn ánh sáng tự nhiên và sự luân chuyển hài hòa giữa kiến trúc hiện đại và sự tĩnh lặng nhiệt đới.")

    # Final audit comprehensive translations
    # Wellness details
    html = html.replace(">Our Spa & wellness<", ">Spa & Chăm sóc sức khỏe<")
    html = html.replace(">Our Spa &amp; wellness<", ">Spa & Chăm sóc sức khỏe<")
    html = html.replace("Our Spa & wellness", "Spa & Chăm sóc sức khỏe")
    html = html.replace("Our Spa &amp; wellness", "Spa & Chăm sóc sức khỏe")
    html = html.replace(">Dining<", ">Ẩm thực<")
    html = html.replace(">Dining </div>", ">Ẩm thực </div>")
    html = html.replace("Perched above the ocean, our open-air pavilion invites you to flow with the rhythm of nature.", "Tọa lạc trên đồi hướng biển, pavilion ngoài trời của chúng tôi mời bạn thả mình theo nhịp điệu của thiên nhiên.")
    html = html.replace(">Healing<", ">Chữa lành<")
    html = html.replace(">Aroma Rituals<", ">Trị liệu hương thơm<")
    html = html.replace("Gentle pressure points to relieve tension and restore energy", "Ấn huyệt nhẹ nhàng để giải tỏa căng thẳng và phục hồi năng lượng")
    html = html.replace("Heated herbal poultices soothe muscles and ease circulation", "Chườm thảo dược ấm làm dịu cơ bắp và hỗ trợ tuần hoàn")
    html = html.replace("Assisted stretches to enhance flexibility and deep relaxation", "Kéo giãn cơ nhẹ nhàng giúp tăng độ dẻo dai và thư giãn sâu")
    html = html.replace("*All treatments are subject to availability and advance booking is recommended.", "*Tất cả liệu trình phụ thuộc vào tình trạng đặt trước, chúng tôi khuyên bạn nên đặt lịch sớm.")
    html = html.replace(">Rituals<", ">Nghi thức trị liệu<")
    html = html.replace("Healing oils and flowing strokes for complete calm", "Tinh dầu phục hồi và các động tác massage dịu nhẹ mang lại cảm giác thư thái hoàn toàn")
    html = html.replace(">Flower Essence Bath<", ">Tắm tinh chất hoa<")
    html = html.replace("A fragrant soak infused with local botanicals", "Ngâm mình thư giãn trong hương hoa thơm mát từ cỏ cây địa phương")
    html = html.replace("Body scrub, aromatherapy massage, and nourishing facial", "Tẩy tế bào chết toàn thân, massage trị liệu hương thơm và dưỡng da mặt chuyên sâu")
    html = html.replace("Side-by-side massage, flower bath, and sparkling wine", "Massage đôi tình nhân bên nhau, tắm hoa lãng mạn và thưởng thức vang nổ")
    
    # Popular packages & kid benefits
    html = html.replace("Complimentary pool floaties & toys for kids", "Miễn phí phao bơi và đồ chơi dưới nước cho bé")
    html = html.replace("Complimentary pool floaties &amp; toys for kids", "Miễn phí phao bơi và đồ chơi dưới nước cho bé")
    html = html.replace("Free kids’ meals (lunch & dinner when dining with parents)", "Miễn phí bữa ăn cho trẻ em (bữa trưa & tối khi dùng bữa cùng bố mẹ)")
    html = html.replace("Free kids’ meals (lunch &amp; dinner when dining with parents)", "Miễn phí bữa ăn cho trẻ em (bữa trưa & tối khi dùng bữa cùng bố mẹ)")
    html = html.replace("Spa & Spa & wellness Appointment", "Đặt lịch Spa & Chăm sóc sức khỏe")
    html = html.replace("Spa &amp; Spa &amp; wellness Appointment", "Đặt lịch Spa & Chăm sóc sức khỏe")
    html = html.replace("Spa & wellness Appointment", "Đặt lịch Spa & Chăm sóc sức khỏe")
    html = html.replace("Spa &amp; wellness Appointment", "Đặt lịch Spa & Chăm sóc sức khỏe")
    html = html.replace("Spa &amp; wellness Escape - Ke Go Retreat Luxury - HTML website template", "Gói Wellness Escape — Ke Go Retreat Hà Tĩnh")
    html = html.replace("Spa & wellness Escape - Ke Go Retreat Luxury - HTML website template", "Gói Wellness Escape — Ke Go Retreat Hà Tĩnh")

    # Titles and other items
    html = html.replace("Not Found - Ke Go Retreat Luxury - HTML website template", "Trang không tìm thấy — Ke Go Retreat Hà Tĩnh")
    html = html.replace("Blog - Ke Go Retreat Luxury - HTML website template", "Trang tin tức & chia sẻ — Ke Go Retreat Hà Tĩnh")

    # Regex for remaining HTML website template titles
    html = re.sub(r' - Ke Go Retreat Luxury -\\s+HTML website template', ' — Ke Go Retreat Hà Tĩnh', html, flags=re.I)

    # Extra common wellness
    html = html.replace("Spa & wellness", "Spa & Chăm sóc sức khỏe")
    html = html.replace("Spa &amp; wellness", "Spa & Chăm sóc sức khỏe")
    html = html.replace("Spa & Wellness", "Spa & Chăm sóc sức khỏe")
    html = html.replace("Spa &amp; Wellness", "Spa & Chăm sóc sức khỏe")
    html = html.replace("Flower Essence Bath", "Tắm tinh chất hoa")
    html = html.replace("The Spa", "Khu Spa")
    html = html.replace("Our Spa", "Khu Spa")
    html = html.replace(">The </div>", ">Khu </div>")
    html = html.replace(">Healing<", ">Chữa lành<")
    html = html.replace("Healing", "Chữa lành")

    # Extra from / Our story
    html = html.replace(">from</div>", ">từ</div>")
    html = html.replace(">from </div>", ">từ </div>")
    html = html.replace("from $", "từ $")
    html = html.replace("Our story", "Câu chuyện của chúng tôi")
    html = html.replace("Our Story", "Câu chuyện của chúng tôi")
    html = html.replace("Our Heritage", "Di sản của chúng tôi")
    html = html.replace("Our Vision", "Tầm nhìn của chúng tôi")
    html = html.replace(">Our </div>", ">Chúng tôi </div>")
    html = html.replace(">Our<", ">Chúng tôi<")
    html = html.replace("Our <em>Story</em>", "Hành trình <em>của chúng tôi</em>")

    # Extra specific wellness categories
    html = html.replace('The <em class="wood-700-text">Ke Go Retreat Spa</em>', 'Không gian <em class="wood-700-text">Ke Go Retreat Spa</em>')
    html = html.replace('Traditional <em class="wood-700-text">Therapies</em>', 'Liệu pháp <em class="wood-700-text">truyền thống</em>')
    html = html.replace('Traditional Therapies', 'Liệu pháp truyền thống')
    html = html.replace('Therapies', 'Liệu pháp')
'''

ANCHOR = "    if \"asatha-hide-vendor\" not in html and \"copyright-flowcub\" in html:"
if ANCHOR in src:
    src = src.replace(ANCHOR, NEW_REPLACEMENTS + "    " + ANCHOR.lstrip(), 1)
    changes.append("OK: new replacements inserted")
else:
    changes.append("MISS: anchor for new replacements not found")

with open(PATH, "w", encoding="utf-8") as f:
    f.write(src)

for c in changes:
    print(c.encode('ascii', errors='replace').decode('ascii'))
print("Done.")
