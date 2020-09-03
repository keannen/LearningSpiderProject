import asyncio
import tkinter

from pyppeteer import launch
import random

def screen_size():
    # use tkinter get screen_size
    tk = tkinter.Tk()
    width = tk.winfo_screenwidth()
    height = tk.winfo_screenheight()
    tk.quit()
    return {'width': width, 'height': height}

async def main():

    browser = await launch(headless=False, args=['--disable-infobars', '--start-maximized'])  # 建立浏览器对象 全屏打开
    page = await browser.newPage()  # 打开新的标签页
    await page.setViewport(screen_size()) # 内容全屏
    await page.setUserAgent("Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5")  # 设置user—agent
    # 规避webdriver检测
    await page.evaluateOnNewDocument('() =>{ Object.defineProperties(navigator,''{ webdriver:{ get: () => false } }) }')
    # 访问目标url 设置网络延时
    # await page.goto('https://www.baidu.com/', options={'timeout': 5 * 1000})
    await page.goto('https://www.jd.com/', options={'timeout': 5 * 1000})

    await asyncio.sleep(5)
    # 搜索框输入 pyppeteer爬虫
    await page.type('#h|keycount|head|search_c', '爬虫书')
    await asyncio.sleep(5)
    # 点击百度一下
    await page.click('#h|keycount|head|search_a')
    await asyncio.sleep(5)
    # await page.mouse.click(1157, 240);
    # 休眠
    await asyncio.sleep(5)
    # await asyncio.sleep(random.uniform(1,2))
    # 关闭浏览器
    await browser.close()

# 启动程序
asyncio.get_event_loop().run_until_complete(main())