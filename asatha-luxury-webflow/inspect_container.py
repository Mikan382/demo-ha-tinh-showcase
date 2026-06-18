import re

with open("assets/cdn.prod.website-files.com/68f0d3dd9d3c1fec17146b9f/css/asatha-luxury-webflow-template.webflow.shared.9a34a6ad6.css", "r", encoding="utf-8") as f:
    css = f.read()

# find all blocks for .container
matches = re.finditer(r"([^\}]*?\.container\s*\{[^\}]*\})", css)
for m in matches:
    print(m.group(1))
    print("-" * 40)
