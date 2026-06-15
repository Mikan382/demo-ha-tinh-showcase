#!/usr/bin/env python3
"""Visual check - capture screenshots of all templates"""
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
OUTPUT_DIR = Path("_visual-audit/current")

async def capture_template(page, template_id, template_name):
    """Capture screenshot of a template"""
    url = f"{BASE_URL}/{template_id}/index.html"
    output_file = OUTPUT_DIR / f"{template_id}.png"
    
    print(f"📸 Capturing {template_name}...")
    
    try:
        await page.goto(url, wait_until="networkidle", timeout=15000)
        await page.wait_for_timeout(2000)  # Let animations settle
        
        # Full page screenshot
        await page.screenshot(path=str(output_file), full_page=True)
        
        # Get page title and check for errors
        title = await page.title()
        
        # Check for visible English text patterns (sample)
        content = await page.content()
        issues = []
        
        if "Book Now" in content and template_id not in ["moonlit-react"]:
            issues.append("⚠️ 'Book Now' found (should be Vietnamese)")
        if "Discover" in content and template_id not in ["asatha-luxury-webflow"]:
            issues.append("⚠️ 'Discover' found")
        if "Welcome to" in content:
            issues.append("⚠️ 'Welcome to' found")
            
        # Check for broken images
        img_count = await page.locator("img").count()
        broken_imgs = await page.locator('img[src*="404"]').count()
        
        status = "✅" if not issues else "⚠️"
        print(f"{status} {template_name}")
        print(f"   Title: {title}")
        print(f"   Images: {img_count} total, {broken_imgs} broken")
        if issues:
            for issue in issues:
                print(f"   {issue}")
        print(f"   Saved: {output_file}")
        
        return {
            "template": template_name,
            "url": url,
            "title": title,
            "img_count": img_count,
            "broken_imgs": broken_imgs,
            "issues": issues,
            "screenshot": str(output_file)
        }
        
    except Exception as e:
        print(f"❌ Error capturing {template_name}: {e}")
        return None

async def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print("🚀 Starting visual audit...")
    print(f"📂 Output: {OUTPUT_DIR}")
    print()
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})
        
        results = []
        for template_id, template_name in TEMPLATES:
            result = await capture_template(page, template_id, template_name)
            if result:
                results.append(result)
            print()
        
        await browser.close()
    
    print("\n" + "="*60)
    print("📊 VISUAL AUDIT SUMMARY")
    print("="*60)
    
    ok_count = sum(1 for r in results if not r["issues"])
    issue_count = sum(1 for r in results if r["issues"])
    
    print(f"✅ No issues: {ok_count}/{len(results)}")
    print(f"⚠️ Has issues: {issue_count}/{len(results)}")
    
    if issue_count > 0:
        print("\n⚠️ Templates with issues:")
        for r in results:
            if r["issues"]:
                print(f"  • {r['template']}: {len(r['issues'])} issues")

if __name__ == "__main__":
    asyncio.run(main())
