import asyncio
from PIL import Image
from playwright.async_api import async_playwright as Playwright
async def render_html(save_path):
    async with Playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        with open("../docs/meme_keywords.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        await page.set_content(html_content)
        await page.screenshot(path=save_path, full_page=True)
        await page.close()
async def compress(image_path,save_path):
    img = Image.open(image_path)
    img = img.convert("RGB")
    img.save(save_path, quality=70)
async def main():
    await render_html("../docs/screenshot.png")
    await compress("../docs/screenshot.png","../docs/compressed.jpg")
asyncio.run(main())