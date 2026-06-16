#!/usr/bin/env python3
"""
Fix the footer translateX(-50%) layout bug in mountain-lodge-framer pages.

Root cause:
  Framer SSR uses transform: translateX(-50%) on the footer's inner container
  combined with position: absolute; left: 50% to center the content.
  Without full JS hydration (local server), the left:50% is missing,
  so columns 2 & 3 are pushed off-screen to the right.

Fix:
  Inject a <style> block that overrides the problematic transforms to
  use standard flexbox centering instead.
"""
import os
import re

pages_dir = r"c:\scratch\demo-ha-tinh-showcase\mountain-lodge-framer"

CSS_FIX = """<style id="mountain-lodge-footer-fix">
/* Fix Framer footer translateX(-50%) layout without JS hydration */
.framer-1wbzjnv { overflow: visible !important; }

/* The inner row that holds Address / Site Links / Follow columns */
.framer-a77uan {
  transform: none !important;
  left: auto !important;
  position: relative !important;
  display: flex !important;
  flex-direction: row !important;
  justify-content: space-between !important;
  align-items: flex-start !important;
  gap: 40px !important;
  width: 100% !important;
  max-width: 1200px !important;
  margin: 0 auto !important;
  padding: 60px 40px 40px !important;
}

/* Bottom bar: Privacy / Terms / Brand name */
.framer-14vf6a1 {
  transform: none !important;
  left: auto !important;
  position: relative !important;
  display: flex !important;
  flex-direction: row !important;
  justify-content: space-between !important;
  align-items: center !important;
  width: 100% !important;
  max-width: 1200px !important;
  margin: 0 auto !important;
  padding: 20px 40px !important;
}

/* Ensure the outer wrapper doesn't clip columns */
.framer-1pi21bt-container,
.framer-QQAjh.framer-1cbyov8 {
  overflow: visible !important;
  width: 100% !important;
}

/* Newsletter section fix - should have proper height */
.framer-1gcfcfp {
  min-height: auto !important;
}

/* Mobile responsiveness */
@media (max-width: 809px) {
  .framer-a77uan {
    flex-direction: column !important;
    gap: 30px !important;
    padding: 40px 20px 30px !important;
  }
  .framer-14vf6a1 {
    flex-direction: column !important;
    gap: 15px !important;
    padding: 20px !important;
    text-align: center !important;
  }
}

@media (min-width: 810px) and (max-width: 1199px) {
  .framer-a77uan {
    padding: 60px 30px 40px !important;
    gap: 25px !important;
  }
  .framer-14vf6a1 {
    padding: 20px 30px !important;
  }
}
</style>"""

INJECTION_ANCHOR = "</head>"

html_files = [
    f for f in os.listdir(pages_dir)
    if f.endswith(".html") and not f.startswith("screenshot")
]
html_files.sort()

print(f"Found {len(html_files)} HTML pages in mountain-lodge-framer")

fixed_count = 0
already_count = 0

for filename in html_files:
    filepath = os.path.join(pages_dir, filename)
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    if "mountain-lodge-footer-fix" in content:
        print(f"  SKIP (already patched): {filename}")
        already_count += 1
        continue

    if INJECTION_ANCHOR not in content:
        print(f"  WARN (no </head>): {filename}")
        continue

    new_content = content.replace(INJECTION_ANCHOR, CSS_FIX + "\n" + INJECTION_ANCHOR, 1)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"  FIXED: {filename}")
    fixed_count += 1

print(f"\nDone: {fixed_count} pages fixed, {already_count} already patched.")
