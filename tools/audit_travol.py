#!/usr/bin/env python3
"""Audit travol-duruthemes core pages against showcase spec."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "travol-duruthemes"
CORE = ["index.html", "about.html", "tours.html", "destination.html", "gallery.html", "contact.html"]

EN_PATTERNS = [
    ("Home", r">Home<"),
    ("About Us", r"About Us"),
    ("Contact Us", r"Contact Us"),
    ("Book Now", r"Book Now"),
    ("Read More", r"Read More"),
    ("Learn More", r"Learn More"),
    ("Europe", r"\bEurope\b"),
    ("Italy", r"\bItaly\b"),
    ("France", r"\bFrance\b"),
    ("Lorem", r"Lorem ipsum"),
    ("travolagency", r"travolagency"),
    ("Discover", r">Discover<|Discover the world"),
    ("Our Tours", r"Our Tours"),
    ("Travel Agency Inc", r"Travel Agency Inc"),
    ("Switzerland", r"Switzerland"),
    ("Perugia", r"Perugia"),
    ("Day Tour", r"\d Day[s]? Tour"),
    ("Guest review", r"Guest review"),
    ("Quisque", r"Quisque imperdiet"),
]

SPEC = {
    "index.html": {
        "must_have": [
            "Khám phá Hà Tĩnh",
            "Thiên Cầm",
            "shared-images",
            "Trang chủ",
            "HA TINH",
        ],
        "title": "Ha Tinh Travel",
    },
}


def check_images(html: str, page: str) -> list[str]:
    issues = []
    clients_hidden = "travol-hide-clients" in html
    for m in re.finditer(r'src="([^"]+)"', html):
        src = m.group(1)
        if src.startswith("http"):
            continue
        if "shared-images" in src:
            continue
        if any(x in src for x in (".svg", "favicon", "/clients/")):
            continue
        if clients_hidden and "/clients/" in src:
            continue
        if "duruthemes.com" in src and "/img/" in src:
            issues.append(f"broken img: {src[:80]}")
    return issues[:8]


def main():
    print("=== TRAVOL CORE AUDIT ===\n")
    all_ok = True
    for page in CORE:
        fp = ROOT / page
        if not fp.exists():
            print(f"[FAIL] {page}: MISSING")
            all_ok = False
            continue
        html = fp.read_text(encoding="utf-8", errors="ignore")
        hits = [name for name, pat in EN_PATTERNS if re.search(pat, html, re.I)]
        imgs = check_images(html, page)
        si = html.count("shared-images")
        print(f"--- {page} ---")
        print(f"  shared-images refs: {si}")
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
        # nav
        for label in ["Trang chủ", "Giới thiệu", "Tour", "Điểm đến", "Thư viện", "Liên hệ"]:
            if label not in html:
                print(f"  nav missing: {label}")
                all_ok = False
        print()
    print("RESULT:", "PASS" if all_ok else "NEEDS FIX")


if __name__ == "__main__":
    main()
