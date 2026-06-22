import os
import re

html_dir = r'c:\scratch\demo-ha-tinh-showcase\asatha-luxury-webflow'

vietnamese_chars = set('àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ')

def is_english(text):
    text = text.strip()
    if not text:
        return False
    if len(text) < 2:
        return False
    # If contains any Vietnamese chars, it's not English
    if any(c in vietnamese_chars for c in text):
        return False
    # Only consider it if it has standard letters
    if not re.search(r'[A-Za-z]', text):
        return False
    # Skip standard symbols, prices
    if re.match(r'^\$?\d+(\.\d+)?$', text):
        return False
    # Skip Webflow JSON or script content
    if '{' in text or '}' in text or 'function(' in text:
        return False
    return True

phrases = set()

for filename in os.listdir(html_dir):
    if not filename.endswith('.html'):
        continue
    filepath = os.path.join(html_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract text between > and <
    # Also need to consider standalone text, but usually it's in tags
    matches = re.findall(r'>([^<]+)<', content)
    for m in matches:
        m = m.strip()
        if is_english(m):
            phrases.add(m)

with open(r'c:\scratch\demo-ha-tinh-showcase\english_phrases.txt', 'w', encoding='utf-8') as f:
    for p in sorted(phrases):
        f.write(p + '\n')

print(f"Extracted {len(phrases)} english phrases")
