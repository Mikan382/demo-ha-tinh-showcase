#!/usr/bin/env python3
"""Text content audit - check for English text"""
import asyncio
from playwright.async_api import async_playwright

TEMPLATES = [
    "wanderway-framer",
    "mountain-lodge-framer",
    "luxestay-framer",
    "asatha-luxury-webflow",
]

BASE_URL = "http://localhost:8080"

async def audit_text(page, template_id):
    url = f"{BASE_URL}/{template_id}/index.html"
    
    print(f"\n{'='*60}")
    print(f"📝 {template_id}")
    print('='*60)
    
    await page.goto(url, wait_until="domcontentloaded", timeout=10000)
    await page.wait_for_timeout(1500)
    
    # Get all text content
    text = await page.locator("body").inner_text()
    
    # English patterns to check
    en_keywords = [
        "Book Now", "Welcome to", "Discover", "Contact Us", "About Us",
        "Traveler", "with us", "Let Us Take You", "Step outside",
        "More than a way", "From serene", "One Happy"
    ]
    
    print("\n🔍 English text found:")
    found_any = False
    for keyword in en_keywords:
        if keyword in text:
            # Get context (50 chars before and after)
            idx = text.find(keyword)
            start = max(0, idx - 50)
            end = min(len(text), idx + len(keyword) + 50)
            context = text[start:end].replace('\n', ' ')
            print(f"  ⚠️ '{keyword}'")
            print(f"     Context: ...{context}...")
            found_any = True
    
    if not found_any:
        print("  ✅ No common English patterns found")
    
    # Sample first 500 chars
    print(f"\n📄 First 500 chars:")
    print(text[:500])

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        
        for template_id in TEMPLATES:
            try:
                await audit_text(page, template_id)
            except Exception as e:
                print(f"❌ Error: {e}")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
