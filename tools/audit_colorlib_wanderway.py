#!/usr/bin/env python3
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]

COLORLIB_CORE = ["index.html", "about.html", "rooms.html", "restaurant.html", "contact.html"]
COLORLIB_NAV = ["Trang chủ", "Phòng", "Ẩm thực", "Giới thiệu", "Liên hệ"]
COLORLIB_MUST = ["Deluxe Hotel", "shared-images", "Hà Tĩnh"]
COLORLIB_INDEX = ["Lựa chọn lưu trú"]

WANDER_CORE = ["index.html", "about-us.html", "tours.html"]
WANDER_NAV = ["Giới thiệu", "Tour", "Đặt tour"]
WANDER_MUST = ["Wander", "shared-images", "Hà Tĩnh"]
WANDER_INDEX = ["Đi Hà Tĩnh"]

EN = [
    ("Home", r">Home<"),
    ("Book Now", r"Book Now"),
    ("Lorem", r"Lorem ipsum|Little Blind Text"),
    ("Europe", r"\bEurope\b"),
    ("Miami", r"Miami"),
    ("Travel and Tourism Template", r"Travel and Tourism Template"),
    ("per night", r"per night"),
    ("View Room", r"View Room Details"),
    ("Check-in", r"Check-in Date"),
    ("Send Message", r"Send Message"),
    ("Happy Guests", r"Happy Guests"),
    ("Our Menu", r"Our Menu"),
    ("Our Restaurants", r"Our Restaurants"),
    ("Buy this template", r"Buy this template"),
    ("Chào mừng To", r"Chào mừng To"),
    ("Liên hệ Us", r"Liên hệ Us"),
]


def en_hits(html: str) -> list[str]:
    return [n for n, p in EN if re.search(p, html, re.I)]


def img_issues(html: str, slug: str) -> list[str]:
    out = []
    for m in re.finditer(r'<img\b[^>]*\ssrc="([^"]+)"', html):
        src = m.group(1)
        if src.startswith("http") or "shared-images" in src:
            continue
        if src.endswith(".svg"):
            continue
        if slug == "colorlib-deluxe" and src.startswith("images/"):
            out.append(src[:70])
        if slug == "wanderway-framer" and "framerusercontent.com" in src and not src.startswith("assets/"):
            out.append(src[:70])
    return out[:6]


def audit(name, folder, core, nav, must, index_must):
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
        imgs = img_issues(html, folder)
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


if __name__ == "__main__":
    c = audit("COLORLIB", "colorlib-deluxe", COLORLIB_CORE, COLORLIB_NAV, COLORLIB_MUST, COLORLIB_INDEX)
    w = audit("WANDERWAY", "wanderway-framer", WANDER_CORE, WANDER_NAV, WANDER_MUST, WANDER_INDEX)
    print("\nOVERALL:", "PASS" if c and w else "NEEDS FIX")
