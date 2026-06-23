import os
import glob
import re

dir_path = r'c:\scratch\demo-ha-tinh-showcase\travol-duruthemes'
html_files = glob.glob(os.path.join(dir_path, '*.html'))

for file_path in html_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove the empty video tag completely
    # <video class="video" src="#" autoplay loop muted></video>
    content = re.sub(r'<video[^>]*src="#"[^>]*>.*?</video>', '', content, flags=re.DOTALL)
    
    # Also handle self closing or other variants if any
    content = re.sub(r'<video[^>]*src="#"[^>]*/>', '', content)

    # Some might have <source src="#">
    content = re.sub(r'<source[^>]*src="#"[^>]*>', '', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Fixed empty video tags in {len(html_files)} files in travol-duruthemes.")
