import os
import glob
import re

dir_path = r'c:\scratch\demo-ha-tinh-showcase\colorlib-deluxe'
html_files = glob.glob(os.path.join(dir_path, '*.html'))

for file_path in html_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove GA tags
    content = re.sub(r'<script[^>]*src="assets/www\.google-analytics\.com/analytics\.js"[^>]*></script>', '', content)
    content = re.sub(r'<script[^>]*src="assets/www\.googletagmanager\.com/gtag/js[^>]*></script>', '', content)
    content = re.sub(r'<script>\(function\(w,i,g\).*?gtag\(\'config\', \'G-[A-Z0-9]+\'\);\s*</script>', '', content, flags=re.DOTALL)
    
    # Remove Maps tag
    content = re.sub(r'<script[^>]*src="assets/maps\.googleapis\.com/maps/api/js[^>]*></script>', '', content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Cleaned up {len(html_files)} files in colorlib-deluxe.")
