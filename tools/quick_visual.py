#!/usr/bin/env python3
"""Quick visual check - just check viewport, not full page"""
import asyncio
from playwright.async_api import async_playwright
from pathlib import Path

TEMPLATES = [
    ("travol-duruthemes", "Ha Tinh Travel"),
    ("hotale-resort", "Thien Cam Resort"),
    ("asatha-luxury-webflow", "Ke Go Retreat"),
    ("moonlit-react", "Moonlit Hotel"),
    ("colorlib-deluxe", "Deluxe Hotel"),
    ("wanderway-framer", "Wander Ha Tinh"),
    ("mountain-lodge-framer", "Ke Go Eco Lodge"),
    ("luxestay-framer", "LuxeStay Ha Tinh"),
]

BASE_URL = "http://localhost:8080"

async def check_template(page, template_id, template_name):
    """Quick check of a template"""
    url = f"{BASE_URL}/{template_id}/index.html"
    
    print(f"🔍 {template_name}...", end=" ", flush=True)
    
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=10000)
        await page.wait_for_timeout(1500)
        
        # Get visible text from body
        body_text = await page.locator("body").inner_text()
        
        # Basic checks
        issues = []
        
        # Check for English patterns (ignoring certain allowed contexts)
        en_patterns = [
            ("Book Now", "should be 'Đặt phòng'"),
            ("Welcome to", "should be Vietnamese"),
            ("Discover", "check if in wrong context"),
            ("Contact Us", "should be 'Liên hệ'"),
            ("About Us", "should be 'Giới thiệu'"),
        ]
        
        for pattern, desc in en_patterns:
            if pattern in body_text:
                # Count occurrences
                count = body_text.count(pattern)
                if count > 0:
                    issues.append(f"'{pattern}' ({count}x)")
        
        # Check for blank/opacity issues
        hidden_elements = await page.locator('[style*="opacity: 0"]').count()
        if hidden_elements > 10:
            issues.append(f"{hidden_elements} hidden elements")
        
        # Get image count
        img_count = await page.locator("img").count()
        
        # Status
        if not issues:
            print(f"✅ OK ({img_count} imgs)")
        else:
            print(f"⚠️ Issues: {', '.join(issues)}")
        
        return {
            "template": template_name,
            "id": template_id,
            "issues": issues,
            "img_count": img_count,
            "hidden_count": hidden_elements
        }
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return {"template": template_name, "id": template_id, "error": str(e)}

async def main():
    print("🚀 Quick visual check (viewport only)\n")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        
        results = []
        for template_id, template_name in TEMPLATES:
            result = await check_template(page, template_id, template_name)
            results.append(result)
        
        await browser.close()
    
    print("\n" + "="*60)
    print("📊 SUMMARY")
    print("="*60)
    
    ok = [r for r in results if not r.get("issues") and not r.get("error")]
    has_issues = [r for r in results if r.get("issues")]
    errors = [r for r in results if r.get("error")]
    
    print(f"✅ Perfect: {len(ok)}/8")
    print(f"⚠️ Has issues: {len(has_issues)}/8")
    print(f"❌ Errors: {len(errors)}/8")
    
    if has_issues:
        print("\n⚠️ Templates needing attention:")
        for r in has_issues:
            print(f"  • {r['template']}: {', '.join(r['issues'])}")
    
    if errors:
        print("\n❌ Templates with errors:")
        for r in errors:
            print(f"  • {r['template']}: {r['error']}")

if __name__ == "__main__":
    asyncio.run(main())
