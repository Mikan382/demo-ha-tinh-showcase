import os

filepath = r'c:\scratch\demo-ha-tinh-showcase\asatha-luxury-webflow\dining.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

replacements = {
    'An experience <em class="wood-700-text">beyond taste</em>': 'Trải nghiệm <em class="wood-700-text">vượt ngoài hương vị</em>',
    'Browse menu': 'Khám phá thực đơn',
    'Ẩm thực <em class="wood-700-text">Experiences</em>': 'Trải nghiệm <em class="wood-700-text">ẩm thực</em>',
    'From hands-on cooking journeys with our chefs to intimate cliffside dinners beneath the stars. Each moment is designed to connect you with Hà Tĩnh’s culture, nature, and spirit — a celebration of flavor, place, and memory.': 'Từ hành trình ẩm thực cùng đầu bếp đến bữa tối riêng tư bên vách đá dưới bầu trời sao. Mỗi khoảnh khắc đều kết nối bạn với văn hóa, thiên nhiên và tinh thần Hà Tĩnh — một sự tôn vinh hương vị, vùng đất và ký ức.',
    '>Starters<': '>Món khai vị<',
    '>Mains<': '>Món chính<',
    '>Desserts<': '>Tráng miệng<',
    '<em>Starters</em>': '<em>Món khai vị</em>',
    'Hà Tĩnhnese <em class="menu-food-name">Tomato Soup</em>': 'Súp Cà Chua <em class="menu-food-name">Hà Tĩnh</em>',
    'Cà chua nướng chậm, gừng và kem dừa': 'Cà chua nướng chậm, gừng và kem dừa',
    '>$18.00<': '>450.000đ<',
    'Green <em class="menu-food-name">Mango Salad</em>': 'Gỏi xoài <em class="menu-food-name">xanh</em>',
    'Crisp mango, fresh herbs, roasted cashews': 'Xoài giòn, rau thơm, hạt điều rang',
    '>$20.00<': '>500.000đ<',
    'Chicken <em class="menu-food-name">Satay</em>': 'Gà <em class="menu-food-name">nướng Satay</em>',
    'Charcoal-grilled skewers, spiced peanut sauce': 'Thịt xiên nướng than, sốt đậu phộng gia vị',
    '>$24.00<': '>600.000đ<',
    'Crispy <em class="menu-food-name">Spring Rolls</em>': 'Chả giò <em class="menu-food-name">giòn rụm</em>',
    'Vegetable filling, chili-lime dip, Chopped mushroom': 'Nhân rau củ, nấm băm, nước chấm chanh ớt',
    '>$16.00<': '>400.000đ<',
    '*Menu items subject to seasonal changes.': '*Các món ăn trong thực đơn có thể thay đổi theo mùa.',
    '<em>Mains</em>': '<em>Món chính</em>',
    'Seared <em class="menu-food-name">Sea Bass</em>': 'Cá chẽm <em class="menu-food-name">áp chảo</em>',
    'Coconut curry, kaffir lime, young vegetables': 'Cà ri dừa, lá chanh kaffir, rau củ non',
    '>$54.00<': '>1.350.000đ<',
    'Braised <em class="menu-food-name">Rib Rendang</em>': 'Sườn bò <em class="menu-food-name">hầm Rendang</em>',
    'Hà Tĩnhnese spices, served with turmeric rice': 'Gia vị Hà Tĩnh, dùng kèm cơm nghệ',
    '>450.000đ<': '>450.000đ<',
    'Vegetarian <em class="menu-food-name">Nasi Campur</em>': 'Cơm chay <em class="menu-food-name">Nasi Campur</em>',
    'Traditional Hà Tĩnhnese plate with assorted plant-based': 'Mâm cơm chay truyền thống Hà Tĩnh',
    '>$38.00<': '>950.000đ<',
    'Grilled Lobster <em class="menu-food-name">sốt me chua ngọt</em>': 'Tôm hùm nướng <em class="menu-food-name">sốt me chua ngọt</em>',
    '>$68.00<': '>1.700.000đ<',
    '<em>Desserts</em>': '<em>Tráng miệng</em>',
    'Coconut <em class="menu-food-name">Crème Brûlée</em>': 'Crème Brûlée <em class="menu-food-name">Dừa</em>',
    'Caramelized top, tropical twist on a classic': 'Lớp đường cháy, biến tấu nhiệt đới từ bản gốc',
    'Mango <em class="menu-food-name">Sticky Rice</em>': 'Xôi <em class="menu-food-name">Xoài</em>',
    'Mango, sweet coconut, pandan-infused rice': 'Xoài, cốt dừa ngọt, xôi lá dứa',
    'Chocolate <em class="menu-food-name">Lava Cake</em>': 'Bánh <em class="menu-food-name">Lava Chocolate</em>',
    'Spiced chocolate, vanilla bean ice cream': 'Chocolate tẩm vị, kem hạt vani',
    '>$20.00/per serve<': '>500.000đ/khẩu phần<'
}

for k, v in replacements.items():
    content = content.replace(k, v)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print('Translations applied to dining.html')
