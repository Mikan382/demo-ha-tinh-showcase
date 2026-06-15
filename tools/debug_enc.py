import sys
sys.path.insert(0, 'tools')

# Read the script file raw bytes
raw = open('tools/fix_luxestay_menu.py', 'rb').read()
idx = raw.find(b'menuItems = [')
print("menuItems raw bytes:", raw[idx:idx+150])
print()

# Now actually import and check the MENU_JS variable
import importlib.util
spec = importlib.util.spec_from_file_location("fix_luxestay_menu", "tools/fix_luxestay_menu.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
idx2 = mod.MENU_JS.find('menuItems')
print("MENU_JS menuItems content:")
print(repr(mod.MENU_JS[idx2:idx2+200]))
print()
print("First label bytes:")
s = mod.MENU_JS[idx2:idx2+200]
print([hex(ord(c)) for c in s[33:50]])
