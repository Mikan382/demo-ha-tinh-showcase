#!/usr/bin/env python3
"""Detailed visual inspection - check what's actually broken"""
import asyncio
from playwright.async_api import async_playwright
from pathlib import Path

async def inspect_template(page, template_id, template_name):
    url = f"http://localhost:8080/{template_id}/index.html"
    output = Path(f"_visual-audit/current/{template_id}.png")
    
    print(f"\n{'='*70}")
    print(f"🔍 {template_name} ({template_id})")
    print('='*70)
    
    await page.goto(url, wait_until="networkidle", timeout=15000)
    await page.wait_for_timeout(2000)
    
    # Take screenshot
    await page.screenshot(path=str(output), full_page=True)
    file_size = output.stat().st_size / 1024 / 1024
    print(f"📸 Screenshot: {output.name} ({file_size:.1f}MB)")
    
    # Get viewport height
    viewport_height = await page.evaluate("window.innerHeight")
    scroll_height = await page.evaluate("document.documentElement.scrollHeight")
    print(f"📏 Page: {scroll_height}px tall (viewport: {viewport_height}px)")
    
    # Check visible text in viewport
    visible_text = await page.locator("body").inner_text()
    text_length = len(visible_text.strip())
    print(f"📝 Text content: {text_length} chars")
    
    # Check for blank sections (sections with no visible content)
    sections = await page.locator("section, div[class*='section'], div[id*='section']").count()
    print(f"📦 Total sections: {sections}")
    
    # Check hidden elements
    hidden = await page.locator('[style*="opacity: 0"], [style*="opacity:0"]').count()
    if hidden > 0:
        print(f"⚠️  Hidden elements (opacity:0): {hidden}")
        
        # Sample first 3 hidden elements
        for i in range(min(3, hidden)):
            el = page.locator('[style*="opacity: 0"], [style*="opacity:0"]').nth(i)
            tag = await el.evaluate("el => el.tagName.toLowerCase()")
            classes = await el.get_attribute("class") or ""
            text_sample = await el.inner_text()
            text_sample = text_sample[:100].strip() if text_sample else "(no text)"
            print(f"   • <{tag}> .{classes[:40]}... → \"{text_sample}\"")
    
    # Check for English keywords
    en_found = []
    keywords = ["Book Now", "Welcome to", "Discover", "Learn More", "Read More", 
                "Contact Us", "About Us", "View All"]
    for kw in keywords:
        if kw in visible_text:
            en_found.append(kw)
    
    if en_found:
        print(f"🌐 English text: {', '.join(en_found)}")
    else:
        print(f"✅ No common English patterns")
    
    # Scroll test - check if content appears after scroll
    print(f"\n🔄 Scroll test...")
    await page.evaluate("window.scrollTo(0, 800)")
    await page.wait_for_timeout(1000)
    
    text_after_scroll = await page.locator("body").inner_text()
    new_content = len(text_after_scroll) - text_length
    
    if new_content > 100:
        print(f"✅ Content loads on scroll (+{new_content} chars)")
    elif hidden > 10:
        print(f"⚠️  Content may be stuck hidden (only +{new_content} chars)")
    
    # Check images
    imgs = await page.locator("img").count()
    broken = await page.locator('img[src=""], img[alt*="404"]').count()
    print(f"🖼️  Images: {imgs} total, {broken} potentially broken")
    
    # Overall verdict
    print(f"\n{'─'*70}")
    issues = []
    if hidden > 15:
        issues.append(f"{hidden} hidden elements")
    if en_found:
        issues.append(f"English: {', '.join(en_found)}")
    if text_length < 500:
        issues.append("Very little text visible")
    
    if not issues:
        print("✅ VERDICT: Looks good!")
    else:
        print(f"⚠️  VERDICT: {' | '.join(issues)}")

async def main():
    templates = [
        ("asatha-luxury-webflow", "Ke Go Retreat"),
        ("wanderway-framer", "Wander Ha Tinh"),
        ("mountain-lodge-framer", "Ke Go Eco Lodge"),
        ("luxestay-framer", "LuxeStay Ha Tinh"),
    ]
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        
        for template_id, name in templates:
            try:
                await inspect_template(page, template_id, name)
            except Exception as e:
                print(f"❌ Error: {e}")
        
        await browser.close()
    
    print(f"\n{'='*70}")
    print("📊 All screenshots saved to _visual-audit/current/")

if __name__ == "__main__":
    asyncio.run(main())
