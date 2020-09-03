import asyncio
from pyppeteer import launch


async def main():
    browser = await launch({'headless': False})
    page = await browser.newPage()
    await page.goto('http://www.4399.com', {'waitUntil': 'networkidle0'})
    await page.click('#login_tologin')
    await asyncio.sleep(1)
    frame = page.frames[1]
    await frame.type('#username', '123456789')
    await frame.type('#j-password', '998765433')
    await asyncio.sleep(5)
    await browser.close()


asyncio.get_event_loop().run_until_complete(main())
