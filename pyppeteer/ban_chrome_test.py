import asyncio
from pyppeteer import launch


async def main():
    browser = await launch(headless=False, args=['--disable-infobars'])
    page = await browser.newPage()
    await page.setUserAgent("Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5")
    await page.evaluateOnNewDocument('() =>{ Object.defineProperties(navigator,'
                                       '{ webdriver:{ get: () => false } }) }')
    await page.setViewport(viewport={'width': 1536, 'height': 768})
    await page.goto('https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html')
    await asyncio.sleep(25)
    await browser.close()


asyncio.get_event_loop().run_until_complete(main())