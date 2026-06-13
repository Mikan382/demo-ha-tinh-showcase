#!/usr/bin/env python3
"""Quick check for known-broken asset patterns."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATTERNS = [
    ("crawl index.htmlassets", r"index\.htmlassets"),
    ("seaside wrong shared path", r"561acb7796da66bb2114da2c/\d+_"),
    ("wanderway remote framer", r"https://framerusercontent\.com/sites/2Z0j"),
    ("colorlib missing images/", r'url\(images/room'),
    ("vendor popup", r"Buy this template"),
]
for slug in ["seaside-webflow", "moonlit-react", "colorlib-deluxe", "wanderway-framer", "luxestay-framer"]:
    folder = ROOT / slug
    if not folder.exists():
        continue
    print(f"=== {slug} ===")
    for name, pat in PATTERNS:
        hits = []
        for fp in folder.glob("*.html"):
            if re.search(pat, fp.read_text(encoding="utf-8", errors="ignore"), re.I):
                hits.append(fp.name)
        if hits:
            print(f"  {name}: {', '.join(hits[:5])}{'...' if len(hits)>5 else ''}")
