import os
import glob
import re

dir_path = r'c:\scratch\demo-ha-tinh-showcase\moonlit-react'
html_files = glob.glob(os.path.join(dir_path, '*.html'))

clean_menu = '''<ul class="list-unstyled">
<li class="slide"><a class="slide__menu__item" href="index.html">Trang chủ</a></li>
<li class="slide"><a class="slide__menu__item" href="room-one.html">Phòng</a></li>
<li class="slide"><a class="slide__menu__item" href="about.html">Giới thiệu</a></li>
<li class="slide"><a class="slide__menu__item" href="blog.html">Tin tức</a></li>
<li class="slide"><a class="slide__menu__item" href="contact.html">Liên hệ</a></li>
</ul>'''

# The list-unstyled tag can be minified, so we'll match <ul class="list-unstyled">...</ul> inside the specific navs
for file_path in html_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix mobile menu
    content = re.sub(r'<nav class="mobile__menu__nav"><ul class="list-unstyled">.*?</ul></nav>', 
                     f'<nav class="mobile__menu__nav">{clean_menu}</nav>', 
                     content, flags=re.DOTALL)
    
    # Fix desktop menu
    content = re.sub(r'<nav class="desktop__menu offcanvas__menu"><ul class="list-unstyled">.*?</ul></nav>', 
                     f'<nav class="desktop__menu offcanvas__menu">{clean_menu}</nav>', 
                     content, flags=re.DOTALL)
                     
    # Also flatten the list into a single line to match minified style if needed, but it's fine
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Fixed navigation for {len(html_files)} files in moonlit-react.")
