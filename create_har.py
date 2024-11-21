import asyncio
import json
from playwright.async_api import async_playwright

def filter_sensitive_info(request):
    sensitive_headers = ["Authorization", "Cookie"]
    filtered_headers = [
        header for header in request.headers if header["name"] not in sensitive_headers
    ]
    request.headers = filtered_headers

async def open_browser_and_wait():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)

        context = await browser.new_context(
            record_har_path="filtered_network_requests.har",  # Path to save the filtered HAR file
            record_har_content="embed",  # Omit content to make the HAR file smaller
        )

        page = await context.new_page()

        context.on("request", filter_sensitive_info)

        print(
            "Browser is open. Press Enter in the terminal when you're ready to close the browser and save cookies..."
        )

        input("Press Enter to continue and close the browser...")

        # Ensure 2FA is completed before saving cookies
        cookies = await context.cookies()

        with open("filtered_cookies.json", "w") as f:
            json.dump(cookies, f, indent=4)

        await context.close()

        await browser.close()

asyncio.run(open_browser_and_wait())
