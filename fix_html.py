import os, glob

for f in glob.glob('asatha-luxury-webflow/*.html'):
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    if '" / đêm</div>' in content:
        content = content.replace('" / đêm</div>', '"> / đêm</div>')
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Fixed {f}")
