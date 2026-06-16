import re

file_path = r"c:\scratch\demo-ha-tinh-showcase\mountain-lodge-framer\index.html"

with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Search for the class framer-Ng8FH in HTML body
matches = re.finditer(r'<[a-z0-9]+[^>]*class="[^"]*framer-Ng8FH[^"]*"[^>]*>', content, re.IGNORECASE)
print("Tags with class framer-Ng8FH:")
for m in matches:
    print(m.group(0)[:300])
