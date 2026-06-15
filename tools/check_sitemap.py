import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
folder = ROOT / "asatha-luxury-webflow"
files = set(f.name for f in folder.glob("*.html"))

print(f"Total HTML files: {len(files)}")
broken_count = 0
for fp in folder.glob("*.html"):
    html = fp.read_text(encoding="utf-8", errors="ignore")
    # Find all href links
    links = re.findall(r'href=["\']([^"\']+\.html(?:#[^"\']*)?)["\']', html)
    for link in links:
        base_link = link.split("#")[0]
        # Ignore external links or empty links
        if base_link.startswith("http") or not base_link:
            continue
        if base_link not in files:
            print(f"{fp.name}: BROKEN -> {link}")
            broken_count += 1

print(f"Broken links found: {broken_count}")
