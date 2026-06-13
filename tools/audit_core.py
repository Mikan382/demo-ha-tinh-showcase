#!/usr/bin/env python3
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = {
    "travol-duruthemes": ["index.html", "about.html", "tours.html", "destination.html", "gallery.html", "contact.html"],
    "hotale-resort": ["index.html", "about-us.html", "room-grid-style-1.html", "price-table.html", "gallery.html", "contact.html"],
    "seaside-webflow": ["index.html", "about.html", "resort.html", "rooms-overview.html", "contact.html"],
    "asatha-luxury-webflow": ["index.html", "about-us.html", "villas-and-suites.html", "wellness.html", "dining.html", "contact-us.html"],
    "colorlib-deluxe": ["index.html", "about.html", "rooms.html", "restaurant.html", "contact.html"],
    "moonlit-react": ["index.html", "about.html", "room-one.html", "gallery.html", "contact.html"],
    "mountain-lodge-framer": ["index.html", "about.html", "rooms.html", "restaurants.html", "contact.html"],
    "wanderway-framer": ["index.html", "about-us.html", "tours.html"],
    "luxestay-framer": ["index.html", "rooms.html", "restaurant.html", "contact-us.html"],
}
PATTERNS = [
    ("Buy this template", r"Buy this template"),
    ("$99", r"\$99"),
    ("Europe", r"Europe"),
    ("Lorem ipsum", r"Lorem ipsum"),
    ("Miami Beach", r"Miami Beach"),
    ("Room Grid Style", r"Room Grid Style"),
    ("More about us", r"More about us"),
    ("Peru", r"\bPeru\b"),
    ("Deluxe Khách sạn", r"Deluxe Khách sạn"),
    ("Seaside - Webflow", r"Seaside - Webflow"),
    (">About<", r">About<"),
    ("Rooms overview", r"Rooms overview"),
]

issues = []
for slug, pages in CORE.items():
    for page in pages:
        fp = ROOT / slug / page
        if not fp.exists():
            issues.append((slug, page, ["MISSING FILE"]))
            continue
        html = fp.read_text(encoding="utf-8", errors="ignore")
        hits = [name for name, pat in PATTERNS if re.search(pat, html, re.I)]
        tpl_dir = ROOT / slug
        has_images = "shared-images" in html
        if not has_images and slug == "seaside-webflow":
            css = tpl_dir / "assets/assets.website-files.com/559ee37b3d3fed5c59f31670/css/template-seaside.webflow.ca9779723.css"
            has_images = css.exists() and "shared-images" in css.read_text(encoding="utf-8", errors="ignore")
        skip_img = page in ("contact.html", "contact-us.html", "price-table.html")
        if (
            slug not in ("mountain-lodge-framer", "wanderway-framer", "luxestay-framer")
            and not has_images
            and not skip_img
        ):
            hits.append("NO shared-images")
        if hits:
            issues.append((slug, page, hits))

print(f"Found {len(issues)} pages with issues:")
for slug, page, hits in issues:
    print(f"  {slug}/{page}: {', '.join(hits)}")
