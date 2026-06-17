#!/usr/bin/env python3
"""Find broken inter-page links in demo templates."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
templates = ["moonlit-react", "colorlib-deluxe", "travol-duruthemes", 
             "asatha-luxury-webflow", "mountain-lodge-framer", "luxestay-framer"]

for t in templates:
    folder = ROOT / t
    if not folder.exists():
        continue
    existing = {f.name for f in folder.glob("*.html")}
    all_links = set()
    for fp in folder.glob("*.html"):
        html = fp.read_text(encoding="utf-8", errors="ignore")
        for m in re.finditer(r'href="([^"#]+\.html)', html):
            url = m.group(1)
            if url.startswith(("http", "//", "javascript")):
                continue
            if "/" in url:
                continue
            all_links.add(url)
    broken = all_links - existing
    if broken:
        print(f"[{t}] Broken links ({len(broken)}):")
        for b in sorted(broken):
            print(f"  - {b}")
    else:
        print(f"[{t}] All links OK")
