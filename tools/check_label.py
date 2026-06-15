import sys
sys.stdout.reconfigure(encoding='utf-8')
f = open('tools/fix_luxestay_menu.py', encoding='utf-8')
content = f.read()
f.close()
idx = content.find('menuItems = [')
s = content[idx:idx+200]
# Print hex values of the label chars
label_start = s.find('label: "') + 8
label_chars = s[label_start:label_start+10]
print('Label chars hex:', [hex(ord(c)) for c in label_chars])
print('Label text:', repr(label_chars))
