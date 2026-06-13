#!/usr/bin/env python3
"""Audit seaside-webflow and moonlit-react core pages."""
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]

SEASIDE_CORE = ["index.html", "about.html", "resort.html", "rooms-overview.html", "contact.html"]
SEASIDE_NAV = ["Trang chủ", "Giới thiệu", "Phòng", "Liên hệ"]
SEASIDE_MUST = ["Coastal Stay", "shared-images", "Thiên Cầm"]
SEASIDE_INDEX = ["Lưu trú gần biển"]

MOONLIT_CORE = ["index.html", "about.html", "room-one.html", "gallery.html", "contact.html"]
MOONLIT_NAV = ["Trang chủ", "Giới thiệu", "Phòng", "Liên hệ"]
MOONLIT_MUST = ["Moonlit", "shared-images", "Hà Tĩnh"]
MOONLIT_INDEX = ["Khách sạn hiện đại"]

EN = [
    ("Home", r">Home<"),
    ("Book Now", r"Book Now"),
    ("Lorem", r"Lorem ipsum"),
    ("Peru", r"\bPeru\b"),
    ("Seaside Hotel", r"Seaside Hotel"),
    ("Webflow", r"Made in Webflow|>Webflow<"),
    ("Netherlands", r"Netherlands"),
    ("Discover more", r"Discover more"),
    ("About Us", r">About Us<"),
    ("Contact Us", r">Contact Us<"),
    ("Moonlit Hotel Hotel", r"Moonlit Hotel Ha Tinh Hotel"),
    ("Bokinn", r">\s*Bokinn\s*<"),
    ("Resturant", r">\s*Resturant\s*<"),
]


def en_hits(html: str) -> list[str]:
    return [name for name, pat in EN if re.search(pat, html, re.I)]


def img_issues(html: str) -> list[str]:
    out = []
    for m in re.finditer(r'<img\b[^>]*\ssrc="([^"]+)"', html):
        src = m.group(1)
        if src.startswith("http") or "shared-images" in src:
            continue
        if src.endswith(".svg"):
            continue
        if "Icon-" in src or "icon-" in src.lower():
            continue
        if "cdn.prod.website-files" in src or "moonlit-react.netlify" in src:
            out.append(src[:85])
        if "561acb7796da66bb" in src and ".jpg" in src:
            out.append(f"cdn jpg: {src[:70]}")
    return out[:6]


def audit(name: str, folder: str, core: list, nav: list, must: list, index_must: list) -> bool:
    print(f"\n=== {name} ===\n")
    ok = True
    base = ROOT / folder
    for page in core:
        fp = base / page
        if not fp.exists():
            print(f"[FAIL] {page}: MISSING")
            ok = False
            continue
        html = fp.read_text(encoding="utf-8", errors="ignore")
        hits = en_hits(html)
        imgs = img_issues(html)
        print(f"--- {page} ---")
        print(f"  shared-images: {html.count('shared-images')}")
        if hits:
            print(f"  EN: {', '.join(hits)}")
            ok = False
        else:
            print("  EN: OK")
        if imgs:
            print(f"  images: {imgs}")
            ok = False
        else:
            print("  images: OK")
        for n in nav:
            if n not in html:
                print(f"  nav missing: {n}")
                ok = False
        for m in must:
            if m not in html:
                print(f"  content missing: {m}")
                ok = False
        if page == "index.html":
            for m in index_must:
                if m not in html:
                    print(f"  hero missing: {m}")
                    ok = False
        print()
    print(f"RESULT {name}:", "PASS" if ok else "NEEDS FIX")
    return ok


def main():
    s = audit("SEASIDE", "seaside-webflow", SEASIDE_CORE, SEASIDE_NAV, SEASIDE_MUST, SEASIDE_INDEX)
    m = audit("MOONLIT", "moonlit-react", MOONLIT_CORE, MOONLIT_NAV, MOONLIT_MUST, MOONLIT_INDEX)
    print("\nOVERALL:", "PASS" if s and m else "NEEDS FIX")


if __name__ == "__main__":
    main()
