import tkinter
import asyncio
from pyppeteer import launch


def screen_size():
    tk = tkinter.Tk()
    width = tk.winfo_screenwidth()
    height = tk.winfo_screenheight()
    tk.quit()
    return {'width': width, 'height': height}


async def main():
    browser = await launch(headless=False, args=['--start-maximized'])  # 页面全屏
    page = await browser.newPage()
    await page.setViewport(screen_size())  # 内容全屏
    await page.goto('https://www.baidu.com/')
    input()
    await browser.close()


asyncio.get_event_loop().run_until_complete(main())
