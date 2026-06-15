import sys
f = open('tools/fix_luxestay_menu.py', 'rb')
raw = f.read()
f.close()
idx = raw.find(b'label: ')
print('Found label at byte:', idx)
print('Raw bytes:', raw[idx:idx+40])
