import asyncio
from pyppeteer import launch


async def main():
    browser = await launch({'headless': False})
    page = await browser.newPage()
    await page.goto('https://www.baidu.com', {'waitUntil': 'networkidle0'})
    el = await page.J('#kw')
    await el.focus()
    await page.keyboard.type('Hello, World!')
    await page.keyboard.press('ArrowLeft')
    await page.keyboard.down('Shift')
    for _ in ' World':
        await page.keyboard.press('ArrowLeft')
    await page.keyboard.up('Shift')
    await page.keyboard.press('Backspace')
    # 结果字符串最终为 'Hello!'
    await asyncio.sleep(5)
    await browser.close()


asyncio.get_event_loop().run_until_complete(main())
