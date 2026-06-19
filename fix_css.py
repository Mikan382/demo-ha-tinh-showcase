css_fix = """
/* HA TINH FIX: Prevent squished background images */
.img, .img-2, .slider-item, .img-wrap {
    background-size: cover !important;
    background-position: center center !important;
    background-repeat: no-repeat !important;
}
"""
css_path = 'c:/scratch/demo-ha-tinh-showcase/colorlib-deluxe/assets/preview.colorlib.com/theme/deluxe/css/style.css'
with open(css_path, 'a', encoding='utf-8') as f:
    f.write(css_fix)
print("CSS appended!")
