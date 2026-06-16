import re

file_path = r"c:\scratch\demo-ha-tinh-showcase\mountain-lodge-framer\index.html"

with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

style_tags = re.findall(r'<style[^>]*>(.*?)</style>', content, re.DOTALL)
tag_content = style_tags[0]

# Split style tag by brackets to find CSS rules
rules = re.findall(r'([^{}]+)\{([^{}]+)\}', tag_content)

print(f"Total CSS rules found in Style Tag 0: {len(rules)}")
for selector, body in rules:
    if any(cls in selector for cls in ['hidden-pjzml6', 'hidden-gqqjl3', 'hidden-1rv7jhb']):
        print(f"Selector: {selector.strip()}")
        print(f"  Body: {body.strip()}")
