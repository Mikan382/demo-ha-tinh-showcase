import sys
from pathlib import Path
import re

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
folder = ROOT / "mountain-lodge-framer"

for fp in folder.glob("*.html"):
    html = fp.read_text(encoding="utf-8", errors="ignore")
    matches = [m.start() for m in re.finditer(r'Culinary Journey', html, re.I)]
    for pos in matches:
        start = max(0, pos - 150)
        end = min(len(html), pos + 150)
        print(f"Match in {fp.name} at {pos}:")
        print(html[start:end])
        print("-" * 50)
