#!/usr/bin/env python3
"""Check for actual blank/invisible sections by measuring visible area"""
import asyncio
from playwright.async_api import async_playwright

async def check_visibility(page, template_id, name):
    url = f"http://localhost:8080/{template_id}/index.html"
    
    print(f"\n{'='*70}")
    print(f"👁️  {name}")
    print('='*70)
    
    await page.goto(url, wait_until="domcontentloaded", timeout=12000)
    await page.wait_for_timeout(2000)
    
    # Scroll through page and check what's visible
    heights = [0, 1000, 2000, 3000, 4000]
    
    for h in heights:
        await page.evaluate(f"window.scrollTo(0, {h})")
        await page.wait_for_timeout(500)
        
        # Get visible text at this scroll position
        visible = await page.evaluate("""
            () => {
                const viewport = {
                    top: window.scrollY,
                    bottom: window.scrollY + window.innerHeight
                };
                
                let visibleText = '';
                let hiddenSections = 0;
                
                // Check all major containers
                const elements = document.querySelectorAll('section, div[class*="section"], main > div, article');
                
                elements.forEach(el => {
                    const rect = el.getBoundingClientRect();
                    const absoluteTop = rect.top + window.scrollY;
                    const absoluteBottom = absoluteTop + rect.height;
                    
                    // Is element in viewport?
                    if (absoluteBottom >= viewport.top && absoluteTop <= viewport.bottom) {
                        const style = window.getComputedStyle(el);
                        const text = el.innerText.trim();
                        
                        if (style.opacity === '0' && text.length > 50) {
                            hiddenSections++;
                        } else if (style.opacity !== '0' && text.length > 10) {
                            visibleText += text.substring(0, 100) + ' ';
                        }
                    }
                });
                
                return {
                    visible: visibleText.substring(0, 200),
                    hidden: hiddenSections
                };
            }
        """)
        
        if visible['hidden'] > 0:
            print(f"📍 Scroll {h}px: ⚠️ {visible['hidden']} sections hidden (có text nhưng opacity:0)")
        
        if visible['visible'].strip():
            preview = visible['visible'][:80].replace('\n', ' ')
            print(f"📍 Scroll {h}px: ✅ Visible text: \"{preview}...\"")
        elif h > 0:
            print(f"📍 Scroll {h}px: ❌ BLANK - không có text hiển thị!")
    
    # Final verdict
    total_hidden = await page.locator('[style*="opacity: 0"], [style*="opacity:0"]').count()
    
    # Check if hidden elements contain important content
    hidden_with_text = await page.evaluate("""
        () => {
            const hidden = document.querySelectorAll('[style*="opacity: 0"], [style*="opacity:0"]');
            let count = 0;
            let samples = [];
            
            hidden.forEach(el => {
                const text = el.innerText?.trim();
                if (text && text.length > 30) {
                    count++;
                    if (samples.length < 3) {
                        samples.push(text.substring(0, 80));
                    }
                }
            });
            
            return {count, samples};
        }
    """)
    
    print(f"\n📊 Summary:")
    print(f"   Total hidden elements: {total_hidden}")
    print(f"   Hidden WITH content: {hidden_with_text['count']}")
    
    if hidden_with_text['count'] > 0:
        print(f"\n⚠️  PROBLEM: {hidden_with_text['count']} sections có nội dung nhưng BỊ ẨN!")
        print(f"   Samples of hidden content:")
        for i, sample in enumerate(hidden_with_text['samples'], 1):
            print(f"   {i}. \"{sample}...\"")
        return False
    else:
        print(f"✅ OK: Hidden elements chỉ là animations/decorations")
        return True

async def main():
    templates = [
        ("asatha-luxury-webflow", "Asatha"),
        ("wanderway-framer", "Wanderway"),
        ("luxestay-framer", "Luxestay"),
        ("mountain-lodge-framer", "Mountain Lodge"),
    ]
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        
        ok_count = 0
        problem_count = 0
        
        for tid, name in templates:
            try:
                is_ok = await check_visibility(page, tid, name)
                if is_ok:
                    ok_count += 1
                else:
                    problem_count += 1
            except Exception as e:
                print(f"❌ Error: {e}")
                problem_count += 1
        
        await browser.close()
        
        print(f"\n{'='*70}")
        print(f"📊 FINAL VERDICT:")
        print(f"✅ OK (hidden = decorations): {ok_count}/4")
        print(f"⚠️  PROBLEM (hidden = content): {problem_count}/4")

if __name__ == "__main__":
    asyncio.run(main())
