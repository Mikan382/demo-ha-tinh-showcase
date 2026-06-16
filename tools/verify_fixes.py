#!/usr/bin/env python3
"""Verify that all fixes were applied correctly."""
import re
import os

# ---- 1. Mountain Lodge: check footer fix injected ----
ml_dir = r"c:\scratch\demo-ha-tinh-showcase\mountain-lodge-framer"
ml_pages = [f for f in os.listdir(ml_dir) if f.endswith(".html")]
ml_pages.sort()

print("=== MOUNTAIN LODGE FOOTER FIX ===")
for fname in ml_pages:
    fpath = os.path.join(ml_dir, fname)
    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    has_fix = "mountain-lodge-footer-fix" in content
    status = "OK" if has_fix else "MISSING"
    print(f"  [{status}] {fname}")

print()

# ---- 2. Colorlib Deluxe: check custom-theme.css linked ----
cd_dir = r"c:\scratch\demo-ha-tinh-showcase\colorlib-deluxe"
cd_pages = [f for f in os.listdir(cd_dir) if f.endswith(".html")]
cd_pages.sort()

print("=== COLORLIB DELUXE CUSTOM THEME ===")
for fname in cd_pages:
    fpath = os.path.join(cd_dir, fname)
    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    has_theme = "custom-theme.css" in content
    status = "OK" if has_theme else "MISSING"
    print(f"  [{status}] {fname}")

print()

# ---- 3. Check custom-theme.css content ----
css_path = r"c:\scratch\demo-ha-tinh-showcase\colorlib-deluxe\assets\preview.colorlib.com\theme\deluxe\css\custom-theme.css"
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8", errors="ignore") as f:
        css = f.read()
    print("=== COLORLIB CUSTOM-THEME.CSS CONTENT CHECK ===")
    print(f"  File size: {len(css)} chars")
    print(f"  Has Playfair Display font: {'Playfair Display' in css}")
    print(f"  Has gold color #D4AF37: {'#D4AF37' in css}")
    print(f"  Has navbar rules: {'.navbar' in css}")
    print(f"  Has overlay rules: {'overlay' in css.lower()}")
    print(f"  Has hero rules: {'hero' in css.lower()}")
    print(f"  Has booking form rules: {'booking' in css.lower()}")
else:
    print("  ERROR: custom-theme.css NOT FOUND!")

print()
print("=== DONE ===")
