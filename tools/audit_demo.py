#!/usr/bin/env python3
"""Deep audit of all 6 demo templates for runtime/demo issues."""
from __future__ import annotations
import re
import os
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = [
    "travol-duruthemes",
    "asatha-luxury-webflow",
    "moonlit-react",
    "mountain-lodge-framer",
    "luxestay-framer",
    "colorlib-deluxe",
]

issues = []

def add(template, page, severity, category, detail):
    issues.append({
        "template": template,
        "page": page,
        "severity": severity,
        "category": category,
        "detail": detail,
    })


def check_internal_links(template, page, html, folder):
    """Check href/src pointing to local files that don't exist."""
    # Find all href and src attributes
    for attr in ("href", "src", "data-background", "poster"):
        for m in re.finditer(rf'{attr}=["\']([^"\'#][^"\']*)["\']', html, re.I):
            url = m.group(1)
            # Skip external URLs, data URIs, javascript:, mailto:, tel:
            if url.startswith(("http://", "https://", "data:", "javascript:", "mailto:", "tel:", "//", "{", "<%")):
                continue
            # Skip anchors
            if url.startswith("#"):
                continue
            # Resolve relative path
            resolved = (folder / unquote(url)).resolve()
            if not resolved.exists():
                add(template, page, "ERROR", "MISSING_ASSET", f'{attr}="{url}" → file not found: {resolved}')


def check_empty_sources(template, page, html):
    """Check for src='#' or empty src."""
    for m in re.finditer(r'src=["\']#["\']', html):
        context = html[max(0, m.start()-50):m.end()+50]
        if "<video" in context.lower() or "<source" in context.lower():
            add(template, page, "WARN", "EMPTY_VIDEO_SRC", f'Video/source with src="#" — will cause console error')
        elif "<img" in context.lower():
            add(template, page, "WARN", "EMPTY_IMG_SRC", f'Image with src="#" — broken image')
        elif "<script" in context.lower():
            add(template, page, "WARN", "EMPTY_SCRIPT_SRC", f'Script with src="#" — may cause loading error')


def check_inline_transforms(template, page, html):
    """Check for problematic inline transforms that cause layout shift."""
    # Owl carousel with pre-baked transform
    for m in re.finditer(r'class="owl-stage"[^>]*style="[^"]*translate3d\((-?\d+)px', html):
        px = int(m.group(1))
        if abs(px) > 100:
            has_fix = "owl-stage{transform:none" in html
            if not has_fix:
                add(template, page, "ERROR", "OWL_TRANSFORM", f'owl-stage has translate3d({px}px) with no CSS fix')
            else:
                add(template, page, "INFO", "OWL_TRANSFORM_FIXED", f'owl-stage has translate3d({px}px) — CSS fix present')


def check_visibility_issues(template, page, html):
    """Check for elements stuck at opacity:0 or visibility:hidden."""
    # Nav menu with opacity:0
    for m in re.finditer(r'class="[^"]*nav-menu[^"]*"[^>]*style="[^"]*opacity:\s*0', html):
        has_fix = "nav-menu" in html and "opacity:1!important" in html
        if not has_fix:
            add(template, page, "ERROR", "NAV_HIDDEN", "Nav menu has inline opacity:0 with no CSS fix")

    # ftco-animate without fix
    if "ftco-animate" in html and "opacity:0" in html:
        has_fix = ".ftco-animate{opacity:1!important" in html
        if not has_fix:
            add(template, page, "ERROR", "FTCO_ANIMATE", "ftco-animate elements start at opacity:0 with no fix")


def check_broken_js_refs(template, page, html, folder):
    """Check for script tags referencing missing JS files."""
    for m in re.finditer(r'<script[^>]+src=["\']([^"\']+)["\']', html, re.I):
        url = m.group(1)
        if url.startswith(("http://", "https://", "//", "data:")):
            continue
        resolved = (folder / unquote(url)).resolve()
        if not resolved.exists():
            add(template, page, "ERROR", "MISSING_JS", f'Script not found: {url}')


def check_broken_css_refs(template, page, html, folder):
    """Check for link tags referencing missing CSS files."""
    for m in re.finditer(r'<link[^>]+href=["\']([^"\']+\.css[^"\']*)["\']', html, re.I):
        url = m.group(1)
        if url.startswith(("http://", "https://", "//", "data:")):
            continue
        # Strip query strings
        clean_url = url.split("?")[0]
        resolved = (folder / unquote(clean_url)).resolve()
        if not resolved.exists():
            add(template, page, "ERROR", "MISSING_CSS", f'CSS not found: {url}')


def check_inter_page_links(template, page, html, folder):
    """Check that internal page links (.html) point to existing files."""
    for m in re.finditer(r'href=["\']([^"\'#]+\.html)(?:#[^"\']*)?["\']', html, re.I):
        url = m.group(1)
        if url.startswith(("http://", "https://", "//", "javascript:")):
            continue
        resolved = (folder / unquote(url)).resolve()
        if not resolved.exists():
            add(template, page, "WARN", "BROKEN_PAGE_LINK", f'Link to missing page: {url}')


def check_preloader(template, page, html):
    """Check if preloader/loader is properly hidden."""
    if "preloader" in html.lower() or "ftco-loader" in html.lower():
        # Check if it has display:none or visibility:hidden
        if 'id="preloader"' in html and 'display: none' not in html.split('id="preloader"')[1][:200]:
            add(template, page, "WARN", "PRELOADER_VISIBLE", "Preloader may be visible on load")
        if 'id="ftco-loader"' in html:
            has_fix = "ftco-loader" in html and ("display:none" in html or "removeClass" in html)
            if not has_fix:
                add(template, page, "WARN", "LOADER_VISIBLE", "ftco-loader may be visible on load")


def check_console_errors(template, page, html):
    """Check for common patterns that cause console errors."""
    # Google Maps API without key
    if "maps.googleapis.com/maps/api/js" in html and "key=" not in html:
        add(template, page, "WARN", "MAPS_NO_KEY", "Google Maps API loaded without API key — will show error overlay")
    
    # Google Analytics to local files
    if "google-analytics.com/analytics.js" in html and 'src="assets/' in html:
        add(template, page, "INFO", "GA_LOCAL", "Google Analytics loaded from local file — will fail silently")
    
    # Broken form actions
    for m in re.finditer(r'action=["\']([^"\']+)["\']', html, re.I):
        action = m.group(1)
        if action.startswith(("http://", "https://")) and "google" not in action:
            add(template, page, "WARN", "FORM_EXTERNAL_ACTION", f'Form posts to external URL: {action}')


def check_image_backgrounds(template, page, html, folder):
    """Check CSS background-image URLs."""
    for m in re.finditer(r'background-image:\s*url\(["\']?([^"\')\s]+)["\']?\)', html, re.I):
        url = m.group(1)
        if url.startswith(("http://", "https://", "data:", "//")):
            continue
        # Handle HTML entity encoding
        url = url.replace("&quot;", "").replace("&amp;", "&")
        resolved = (folder / unquote(url)).resolve()
        if not resolved.exists():
            add(template, page, "ERROR", "MISSING_BG_IMAGE", f'Background image not found: {url}')


def check_hotale_missing():
    """Check if hotale-resort is referenced but exists."""
    hotale = ROOT / "hotale-resort"
    if hotale.exists():
        # Check if it's in the catalog
        catalog = (ROOT / "index.html").read_text(encoding="utf-8", errors="ignore")
        if "hotale" not in catalog.lower():
            add("hotale-resort", "N/A", "INFO", "NOT_IN_CATALOG", "hotale-resort exists but not in catalog")


def audit_template(template):
    folder = ROOT / template
    if not folder.exists():
        add(template, "N/A", "ERROR", "TEMPLATE_MISSING", f"Template folder does not exist: {folder}")
        return
    
    html_files = sorted(folder.glob("*.html"))
    if not html_files:
        add(template, "N/A", "ERROR", "NO_HTML_FILES", "No HTML files found in template folder")
        return
    
    # Check index.html exists
    index = folder / "index.html"
    if not index.exists():
        add(template, "index.html", "ERROR", "NO_INDEX", "index.html missing — catalog link will 404")
        return
    
    for fp in html_files:
        html = fp.read_text(encoding="utf-8", errors="ignore")
        page = fp.name
        
        check_empty_sources(template, page, html)
        check_inline_transforms(template, page, html)
        check_visibility_issues(template, page, html)
        check_broken_js_refs(template, page, html, folder)
        check_broken_css_refs(template, page, html, folder)
        check_inter_page_links(template, page, html, folder)
        check_preloader(template, page, html)
        check_console_errors(template, page, html)
        check_image_backgrounds(template, page, html, folder)
        # Only check internal links for index.html (main demo page) to reduce noise
        if page == "index.html":
            check_internal_links(template, page, html, folder)


def main():
    # Check catalog page
    catalog = ROOT / "index.html"
    if catalog.exists():
        html = catalog.read_text(encoding="utf-8", errors="ignore")
        for m in re.finditer(r'href=["\']([^"\']+/index\.html)["\']', html):
            target = ROOT / m.group(1)
            if not target.exists():
                add("CATALOG", "index.html", "ERROR", "BROKEN_CATALOG_LINK", f'Catalog links to missing page: {m.group(1)}')
        # Check thumbnail images
        for m in re.finditer(r"url\('([^']+)'\)", html):
            img_path = ROOT / m.group(1)
            if not img_path.exists():
                add("CATALOG", "index.html", "ERROR", "MISSING_THUMBNAIL", f'Thumbnail image missing: {m.group(1)}')
    
    # Audit each template
    for template in TEMPLATES:
        print(f"Auditing {template}...")
        audit_template(template)
    
    check_hotale_missing()
    
    # Print results
    print("\n" + "=" * 80)
    print("AUDIT RESULTS")
    print("=" * 80)
    
    errors = [i for i in issues if i["severity"] == "ERROR"]
    warns = [i for i in issues if i["severity"] == "WARN"]
    infos = [i for i in issues if i["severity"] == "INFO"]
    
    if errors:
        print(f"\n[ERROR] ERRORS ({len(errors)}):")
        for i in errors:
            print(f"  [{i['template']}] {i['page']}: [{i['category']}] {i['detail']}")
    
    if warns:
        print(f"\n[WARN] WARNINGS ({len(warns)}):")
        for i in warns:
            print(f"  [{i['template']}] {i['page']}: [{i['category']}] {i['detail']}")
    
    if infos:
        print(f"\n[INFO] INFO ({len(infos)}):")
        for i in infos:
            print(f"  [{i['template']}] {i['page']}: [{i['category']}] {i['detail']}")
    
    if not issues:
        print("\n[OK] No issues found!")
    
    print(f"\nTotal: {len(errors)} errors, {len(warns)} warnings, {len(infos)} info")


if __name__ == "__main__":
    main()
