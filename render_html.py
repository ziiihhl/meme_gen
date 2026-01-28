import asyncio

from playwright.async_api import async_playwright as Playwright
async def main():
    async with Playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        with open("./docs/meme_keywords.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        await page.set_content(html_content)
        await page.screenshot(path="./docs/screenshot.png",full_page=True)
        await page.close()

asyncio.run(main())