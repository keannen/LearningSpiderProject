import asyncio
from pyppeteer import launch


async def main():
    browser = await launch()
    page = await browser.newPage()
    await page.setViewport(viewport={'width': 1280, 'height': 800})

    # 是否启用js
    await page.setJavaScriptEnabled(enabled=True)

    await page.goto('https://www.toutiao.com')

    # 打印cookie页面
    print(await page.cookies())

    # await asyncio.sleep(5)
    await asyncio.sleep(2)
    title_ele = await page.xpath('//div[@class="title-box"]/a')

    for item in title_ele:
        # title_str = await (await item.getProperty('textContent')).jsonValue()
        print(await (await item.getProperty('textContent')).jsonValue())
        title_link = await (await item.getProperty('href')).jsonValue()
        print(title_link)
        # print(await item.jsonValue())

    await browser.close()

    # # 打印页面文本
    # print(await page.content())
    #
    # # 打印当前首页的标题
    # print(await page.title())

asyncio.run(main())