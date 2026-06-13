#!/usr/bin/env python3
"""Audit hotale-resort and asatha-luxury-webflow core pages."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

HOTALE_CORE = [
    "index.html",
    "about-us.html",
    "room-grid-style-1.html",
    "price-table.html",
    "gallery.html",
    "contact.html",
]
HOTALE_NAV = ["Trang chủ", "Giới thiệu", "Phòng", "Gallery", "Liên hệ"]
HOTALE_MUST = ["Thiên Cầm", "shared-images"]
HOTALE_INDEX_MUST = ["Kỳ nghỉ"]

ASATHA_CORE = [
    "index.html",
    "about-us.html",
    "villas-and-suites.html",
    "wellness.html",
    "dining.html",
    "contact-us.html",
]
ASATHA_NAV = ["Giới thiệu", "Villa", "Spa & wellness", "Liên hệ"]
ASATHA_MUST = ["Ke Go", "shared-images", "Hà Tĩnh"]

EN_PATTERNS = [
    ("Home", r">Home<"),
    ("About Us", r">About Us<"),
    ("Book Now", r">Book Now<|>Book Now<"),
    ("Lorem", r"Lorem ipsum"),
    ("Europe", r"\bEurope\b"),
    ("Bali", r"\bBali\b"),
    ("Asatha", r">Asatha<|>Asatha <|Asatha —"),
    ("Hotel HTML Template", r"Hotel HTML Template"),
    ("Flowcub", r">Flowcub<|Powered by Flowcub"),
    ("Madrid", r"Madrid"),
    ("Uluwatu", r"Uluwatu"),
    ("Indian Ocean", r"Indian Ocean"),
    ("wonderful serenity", r"wonderful serenity"),
    ("so absorbed", r"so absorbed"),
    ("Select one", r"Select one"),
    ("Boutique villas", r"Boutique villas"),
    ("Quick Links", r">Quick Links<"),
    ("Homepage", r">Homepage<"),
    ("Check Availability", r"Check <em"),
    ("Discover", r"Discover [A-Z]"),
    ("Read More", r"Read More"),
    ("Subscribe", r">Subscribe<"),
    ("Hotale Av", r"Hotale Av"),
]


def check_images(html: str) -> list[str]:
    issues = []
    for m in re.finditer(r'<img\b[^>]*\ssrc="([^"]+)"', html):
        src = m.group(1)
        if src.startswith("http"):
            continue
        if "shared-images" in src:
            continue
        if src.endswith(".svg") or "logo" in src.lower():
            continue
        if "cdn.prod.website-files.com" in src:
            issues.append(f"cdn img: {src[:80]}")
        if "/upload/" in src and src.endswith((".jpg", ".jpeg", ".png", ".webp")):
            issues.append(f"upload img: {src[:80]}")
    return issues[:6]


def audit_template(name: str, folder: str, core: list[str], nav_labels: list[str], must: list[str]) -> bool:
    print(f"\n=== {name} ===\n")
    all_ok = True
    base = ROOT / folder
    for page in core:
        fp = base / page
        if not fp.exists():
            print(f"[FAIL] {page}: MISSING")
            all_ok = False
            continue
        html = fp.read_text(encoding="utf-8", errors="ignore")
        hits = [n for n, pat in EN_PATTERNS if re.search(pat, html, re.I)]
        imgs = check_images(html)
        si = html.count("shared-images")
        print(f"--- {page} ---")
        print(f"  shared-images: {si}")
        if hits:
            print(f"  EN/vendor: {', '.join(hits)}")
            all_ok = False
        else:
            print("  EN/vendor: OK")
        if imgs:
            print(f"  images: {imgs}")
            all_ok = False
        else:
            print("  images: OK")
        for label in nav_labels:
            if label not in html:
                print(f"  nav missing: {label}")
                all_ok = False
        for m in must:
            if m not in html:
                print(f"  content missing: {m.encode('ascii', 'replace').decode()}")
                all_ok = False
        if page == "index.html" and folder == "hotale-resort":
            for m in HOTALE_INDEX_MUST:
                if m not in html:
                    print(f"  hero missing: {m.encode('ascii', 'replace').decode()}")
                    all_ok = False
        print()
    print(f"RESULT {name}:", "PASS" if all_ok else "NEEDS FIX")
    return all_ok


def main():
    h = audit_template("HOTALE", "hotale-resort", HOTALE_CORE, HOTALE_NAV, HOTALE_MUST)
    a = audit_template("ASATHA", "asatha-luxury-webflow", ASATHA_CORE, ASATHA_NAV, ASATHA_MUST)
    print("\nOVERALL:", "PASS" if h and a else "NEEDS FIX")


if __name__ == "__main__":
    main()
