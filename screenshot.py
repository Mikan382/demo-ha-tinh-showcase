import asyncio
from playwright.async_api import async_playwright
import os

async def take_screenshots():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        urls = [
            'http://127.0.0.1:5503/demo-ha-tinh-showcase/asatha-luxury-webflow/index.html',
            'http://127.0.0.1:5503/demo-ha-tinh-showcase/asatha-luxury-webflow/wellness.html',
            'http://127.0.0.1:5503/demo-ha-tinh-showcase/asatha-luxury-webflow/villas-and-suites.html'
        ]
        
        for url in urls:
            try:
                name = url.split('/')[-1].replace('.html', '')
                await page.goto(url)
                # Wait a bit for animations
                await page.wait_for_timeout(2000)
                path = f'c:/scratch/demo-ha-tinh-showcase/{name}_screenshot.png'
                await page.screenshot(path=path, full_page=True)
                print(f"Screenshot saved to {path}")
            except Exception as e:
                print(f"Failed to screenshot {url}: {e}")
                
        await browser.close()

if __name__ == "__main__":
    asyncio.run(take_screenshots())
