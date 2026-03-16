import asyncio
from playwright.async_api import async_playwright
import os

os.makedirs('assets', exist_ok=True)

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1280, "height": 800})
        print("Navigating to UI...")
        await page.goto("http://localhost:8501", wait_until="networkidle")
        await page.wait_for_timeout(3000)
        
        # Take an initial screenshot in case interaction fails
        await page.screenshot(path="assets/demo_initial.png")
        
        try:
            print("Typing query...")
            # Streamlit chat input usually uses this textarea
            await page.fill('[data-testid="stChatInput"] textarea', 'What is Slooze AI?')
            await page.keyboard.press("Enter")
            print("Waiting for response...")
            await page.wait_for_timeout(15000) # Give it 15 seconds to stream the response
        except Exception as e:
            print("Could not interact with chat input:", e)

        print("Capturing final screenshot...")
        await page.screenshot(path="assets/demo.png")
        await browser.close()
        print("Done.")

asyncio.run(run())
