import os

base_dir = 'c:/scratch/demo-ha-tinh-showcase/colorlib-deluxe'
rest_path = os.path.join(base_dir, 'restaurant.html')
about_path = os.path.join(base_dir, 'about.html')

lodge_img = '19_hospitality_forest_lake_lodge.png'
rest_img = '44_experience_seafood_dinner_beach.png'
about_img = '08_hospitality_hospitality_beachfront_resort.png'

# Fix restaurant.html
if os.path.exists(rest_path):
    with open(rest_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # We just replace the lodge image with a restaurant image
    html = html.replace(lodge_img, rest_img)
    
    with open(rest_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Fixed restaurant.html")

# Fix about.html
if os.path.exists(about_path):
    with open(about_path, 'r', encoding='utf-8') as f:
        html = f.read()
        
    html = html.replace(lodge_img, about_img)
    html = html.replace('Chào mừng đến Deluxe Hotel Ha Tinh', 'Câu Chuyện Về Deluxe Hotel')
    html = html.replace('Deluxe Hotel Ha Tinh mang đến không gian nghỉ dưỡng tiện nghi ven biển Thiên Cầm, phù hợp cho kỳ nghỉ trăng mật và thư giãn tại Hà Tĩnh.', 
                        'Được thành lập với sứ mệnh mang đến trải nghiệm nghỉ dưỡng xa hoa, Deluxe Hotel là biểu tượng của sự thanh lịch và đẳng cấp, mang đậm dấu ấn văn hóa và lòng hiếu khách của dải đất miền Trung.')
    
    with open(about_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Fixed about.html")
