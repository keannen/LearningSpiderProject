import asyncio
import datetime
import tkinter
import pymongo
from lxml import etree
from pyppeteer import launch
import random
# 测试mongo存入数据
"""
    页面分析
    护肤第一页：
    http://mall.jumei.com/?from=Home_show_nav_fresh_new_2
    http://search.jumei.com/?filter=0-11-2&search=%E6%8A%A4%E8%82%A4&bid=4&site=bj
    http://search.jumei.com/?filter=0-11-3&search=%E6%8A%A4%E8%82%A4&bid=4&site=bj
    http://search.jumei.com/?filter=0-11-4&search=%E6%8A%A4%E8%82%A4&bid=4&site=bj
"""

def screen_size():
    # use tkinter get screen_size
    tk = tkinter.Tk()
    width = tk.winfo_screenwidth()
    height = tk.winfo_screenheight()
    tk.quit()
    # print(width,height) # 1366 768 小屏幕  1440 900 大屏幕
    return {'width': width, 'height': height}


async def main():
    # 连接数据库 创建链接对象-》选择数据库-》选择集合
    conn = pymongo.MongoClient('localhost', 27017)
    db = conn['jmypdb']
    myset = db['jmypdb']
    # 计数
    num = 0
    current_page = 0
    start = datetime.datetime.now()
    browser = await launch(headless=True, args=['--disable-infobars', '--start-maximized'])  # 建立浏览器对象 全屏打开
    page = await browser.newPage()  # 打开新的标签页
    await page.setViewport(screen_size())  # 内容全屏
    # 设置请求头
    await page.setUserAgent("Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1")
    # 规避webdriver检测
    await page.evaluateOnNewDocument('() =>{ Object.defineProperties(navigator,''{ webdriver:{ get: () => false } }) }')

    await page.goto('http://search.jumei.com/?filter=0-11-1&search=%E6%8A%A4%E8%82%A4&bid=4&site=bj')

    await asyncio.sleep(3)

    # 滑动到页面底部   不然刚进入页面只渲染出了30条信息  一半
    await page.evaluate('window.scrollBy(0, document.body.scrollHeight)')
    # 休眠   防止爬取过快被返回首页
    await asyncio.sleep(random.randint(3, 5))
    try:
        while True:
            page_info = await page.content()
            html = etree.HTML(page_info)

            goods_title_one = html.xpath('.//div[@class="products_wrap"]/ul/li//div[@class="s_l_name"]/a//text()')
            goods_pid = html.xpath('.//div[@class="products_wrap"]/ul/li/@pid')
            goods_url = html.xpath('.//div[@class="products_wrap"]/ul/li//div[@class="s_l_name"]/a/@href')
            goods_price = html.xpath('//div[@class="products_wrap"]/ul/li//div[@class="search_list_price"]/span//text()')


            good_list = []
            goods_title = []

            # 处理页面标题
            goods_title_text = ''
            for title in goods_title_one:
                goods_title_text += title
            goods_title_text=goods_title_text.split('\n')
            for item in goods_title_text:
                item = item.strip()
                if item:
                    goods_title.append(item.replace(' ', '').replace('\n', ''))
            # print(goods_title)
            # print(len(goods_title))
            # print(len(goods_url))
            # print(len(goods_price))
            # print(len(goods_pid))

            # 解析提取相关数据
            for i in range(len(goods_url)):
                good_info = {}
                good_info['pid'] = goods_pid[i]
                good_info['title'] = goods_title[i]
                good_info['price'] = goods_price[i]
                good_info['url'] = goods_url[i].strip()
                # print('good_info', good_info)
                print('已存入一条数据：', good_info)
                # myset.insert_one(good_info)
                good_list.append(good_info)
                num += 1
            # await asyncio.sleep(3)
            current_page += 1
            myset.insert_many(good_list)
            print('成功将第{}页数据存入mongo'.format(current_page))
            print('当前共存入{}条数据'.format(num))
            await page.click('#search_list_wrap > div.search_list_head_fiex > div > div.head_pagebtn > a.enable.next')
            await asyncio.sleep(5)
            await page.evaluate('window.scrollBy(0, document.body.scrollHeight)')  # 滑动到页面底部
            await asyncio.sleep(5)
    except Exception as e:
        print('程序出错了')
        print(e)

    delta = (datetime.datetime.now() - start).total_seconds()
    print("用时：{:.3f}s".format(delta))
    await browser.close()   # 关闭浏览器


# 启动程序
asyncio.get_event_loop().run_until_complete(main())