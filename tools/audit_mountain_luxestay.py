#!/usr/bin/env python3
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]

MOUNTAIN_CORE = ["index.html", "about.html", "rooms.html", "restaurants.html", "contact.html"]
MOUNTAIN_NAV = ["Phòng", "Liên hệ", "Thư viện"]
MOUNTAIN_MUST = ["Ke Go Eco Lodge", "shared-images", "Hà Tĩnh"]
MOUNTAIN_INDEX = ["Chạm vào nhịp sống xanh"]

LUXESTAY_CORE = ["index.html", "rooms.html", "restaurant.html", "contact-us.html"]
LUXESTAY_NAV = ["Giới thiệu", "Phòng", "Ẩm thực", "Liên hệ"]
LUXESTAY_NAV_SUB = ["Ẩm thực"]
LUXESTAY_MUST = ["LuxeStay", "shared-images", "Hà Tĩnh"]
LUXESTAY_INDEX = ["Không gian nghỉ dưỡng"]

EN = [
    ("Book Now", r"Book Now"),
    ("Home", r">Home<"),
    ("Lorem", r"Lorem ipsum"),
    ("Mountain Lodge", r"Mountain Lodge"),
    ("Ke Go Eco Eco", r"Ke Go Eco Eco"),
    ("BOOK YOUR STAY", r"BOOK YOUR STAY"),
    ("Buy this template", r"Buy this template"),
    ("island living", r"island living"),
    ("Book a stay", r"Book a stay"),
    ("Luxestay", r">Luxestay<"),
    ("Created by uxridham", r"Created by uxridham"),
    ("editor iframe", r'<iframe id="__framer-editorbar"'),
]


def en_hits(html: str) -> list[str]:
    return [n for n, p in EN if re.search(p, html, re.I)]


def img_issues(html: str, slug: str) -> list[str]:
    out = []
    pat = r'(?:src|href)="([^"]+)"'
    for m in re.finditer(pat, html):
        src = m.group(1)
        if src.startswith("http") or "shared-images" in src:
            continue
        if src.endswith(".svg") or ".mjs" in src:
            continue
        if "framerusercontent.com/images" in src and not src.startswith("assets/"):
            out.append(src[:70])
    framer_urls = len(
        re.findall(
            r"url\([^)]*framerusercontent\.com/images/[^)]+\.(?:jpg|jpeg|png|webp)",
            html,
            re.I,
        )
    )
    if framer_urls:
        out.append(f"framer bg urls: {framer_urls}")
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
        page_nav = nav if page == "index.html" else (nav if folder != "luxestay-framer" else LUXESTAY_NAV_SUB)
        for n in page_nav:
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
    m = audit("MOUNTAIN", "mountain-lodge-framer", MOUNTAIN_CORE, MOUNTAIN_NAV, MOUNTAIN_MUST, MOUNTAIN_INDEX)
    l = audit("LUXESTAY", "luxestay-framer", LUXESTAY_CORE, LUXESTAY_NAV, LUXESTAY_MUST, LUXESTAY_INDEX)
    print("\nOVERALL:", "PASS" if m and l else "NEEDS FIX")
