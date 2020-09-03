# -*- coding:utf-8 -*-
# create_time 2020/7/10
# 参考链接https://blog.csdn.net/OYY_90/article/details/88708012
import asyncio
from pyppeteer import launch
import random
from retrying import retry
import time
import re
import random
from lxml import etree


def input_time_random():
    return random.randint(100, 151)


def retry_if_result_none(result):
    return result is None


async def get_task():
    pass


@retry(retry_on_result=retry_if_result_none, )
async def mouse_slide(page=None, frame=None):
    await asyncio.sleep(2)
    try:
        # 鼠标移动到滑块，按下，滑动到头（然后延时处理），松开按键
        if frame:
            await frame.hover('#nc_1_n1z')
        else:
            await page.hover('#nc_1_n1z')
        await page.mouse.down()
        await page.mouse.move(2000, 0, {'delay': random.randint(1000, 2000)})
        await page.mouse.up()
    except Exception as e:
        print(e, ':验证失败')
        return None, page
    else:
        await asyncio.sleep(2)
        # 判断是否通过
        slider_again = ''
        try:
            slider_again = await page.Jeval('.nc-lang-cnt', 'node => node.textContent')
        except:
            pass
        if slider_again != '验证通过':
            return None, page
        else:
            print('验证通过')
            return 1, page


async def parse_live_page(page=None, KOL_live=None, uid=None):
    live_prase = 'https://101.37.172.127:13042/Blogger/LiveSellGoodsAnalyze?uid={uid}'
    await page.goto(live_prase.format(uid=uid))
    await page.waitFor(5000)
    print(1111111111111)
    live_content = await page.content()
    html = etree.HTML(live_content)
    re_obj = re.compile(r'<div class="text">.*?(\w+).*?<div>', re.S)
    live_text = re_obj.findall(live_content)
    while '' in live_text:
        live_text.remove('')
    # 开播时间list
    live_date = html.xpath('//*[@id="zb-record"]/div/div/div[2]/table/tbody/tr/td[2]/span/text()')
    live_time = html.xpath('//*[@id="zb-record"]/div/div/div[2]/table/tbody/tr/td[3]/span/text()')
    roomid = re.findall(r'roomId=(.*) data-toggle', live_content)
    datecode = re.findall(r'dateCode=(.*)&', live_content)
    for item in range(len(live_date)):
        KOL_live['live_text'] = live_text[item]
        KOL_live['live_date'] = live_date[item]
        KOL_live['live_time'] = live_time[item]
        live_detail_url = 'https://101.37.172.127:13042/LiveDetail?dateCode={datecode}&roomId={roomid}'
        await page.goto(live_detail_url.format(datecode=datecode[item], roomid=roomid[item]))
        # 观看人数，音浪数，本厂点赞
        await page.waitFor(3000)
        live_detail_content = await page.content()
        live_html = etree.HTML(live_detail_content)
        watch_people = live_html.xpath('//*[@id="tab1"]/div/div[1]/div/div[2]/div[1]/span/text()')
        dy_count = live_html.xpath('//*[@id="tab1"]/div/div[1]/div/div[2]/div[4]/span/text()')
        video_like = live_html.xpath('//*[@id="tab1"]/div/div[1]/div/div[2]/div[3]/text()[2]')
        gift_count = live_html.xpath('//*[@id="tab1"]/div/div[1]/div/div[2]/div[4]/text()[2]')
        KOL_live['watch_people'] = watch_people[0]
        KOL_live['dy_count'] = dy_count[0]
        KOL_live['video_like'] = video_like[0]
        KOL_live['gift_count'] = gift_count[0]
        print(KOL_live)


async def test():
    browser = await launch(
        {
            'headless': False,
            'dumpio': True,
            'autoClose': True,
            'args': [
                '--no-sandbox',
                '--window-size=1366,850'
            ]
        }
    )
    page = await browser.newPage()
    await page.setViewport({'width': 1366, 'height': 768})
    await page.goto("http://47.93.122.10:16888/admin/index")
    await asyncio.sleep(3)
    await page.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')

    # todo 输入账号和密码
    await page.type("[id=username]", "13826495956", {'delay': input_time_random() - 50})
    await page.type("[id=password]", '''dm123456''', {'delay': input_time_random() - 50})
    await asyncio.sleep(10)





    # TODO 进入搜索页面
    await page.goto('http://101.37.172.127:13042/Member#/LiveBlogger')
    # await page.goto('https://dy.feigua.cn/Member#/LiveBlogger/{}'.format(await get_task()))
    # await asyncio.sleep(6)
    # await page.click('#tagFilter > a:nth-child(3)')
    # await page.click('#tagFilter > a:nth-child(4)')
    # await page.click('#tagFilter > a:nth-child(5)')
    # await page.click('#tagFilter > a:nth-child(6)')
    # await page.click('#ec-categoryFilter > a:nth-child(2)')
    # await page.click('#ec-categoryFilter > a:nth-child(3)')
    # await page.click('#content > div > div.search-top.v-search-head.v-search-head-zbh > div > div.senior-search.js-advanced-options.search-items > div > div.search-item.search-item-list.search-item-select > div.search-item-1 > div > span > span > span.selection > span > span.select2-selection__arrow')

    await page.waitFor(2000)
    # await page.click('.select2-results__options > li:nth-child(2)')
    # await asyncio.sleep(3)
    count=0
    while True:
        if count<100:
            await page.keyboard.press('PageDown')
            await time.sleep(random.randint(3,6))
            count+=1
        else:
            break
    await page.waitFor(5000)
    content1 = await page.content()
    print(content1)
    timestamp_list = re.findall(r';timestamp=(.*?)&', content1)
    signature_list = re.findall(';signature=([0-9a-zA-Z]{4,32})', content1)
    id_list = re.findall(r'id=(.*?)&', content1)
    print(id_list)
    detail_live_url = 'https://101.37.172.127:13042/Blogger/Detail?id={id}&timestamp={timestamp}&signature={signature}'

    first_page_data = {}
    KOL_live = {}
    KOL_data = {}
    KOL_video = {}
    for item in range(len(id_list)):
        # #TODO 直播详情按钮
        button = '#liveRoom_tbodyData > tr:nth-child({item}) > td.text-center > div > a.source-details > i'
        await page.click(button.format(item=item + 1))
        await page.waitFor(5000)
        total_page = await browser.pages()
        print(total_page)
        page2 = total_page[2]
        await page2.setViewport({'width': 1366, 'height': 768})
        await page.waitFor(3000)
        await page2.click('#js-tab_options > li:nth-child(7) > a')
        fan_cotent = await page2.content()
        re_total_fans = re.findall(r'var liveFansClub7 =(.*);', fan_cotent)
        total_fans = re_total_fans[-1]
        # TODO 粉丝团人数
        total_fans_y = total_fans['y']
        print(total_fans_y)


        blogger_video_url='https://101.37.172.127:13042/Blogger/AwemeList?id={id}&page=1&sort=1&hide=1'
        await page.goto(blogger_video_url.format(id=id_list[item]))
        await page.waitFor(2000)
        text = await page.content()
        print('直播详' + text)
        video_html = etree.HTML(text)
        # TODO 根据作品数判断
        count = video_html.xpath('//*[@id="AwemeCount_Data"]/text()')
        # 视频标题，点赞评论转发
        title = video_html.xpath('//*[@id="js-blogger-history-awemes"]/tr/td[1]/div/div[2]/div[1]/a/text()')
        video_like = video_html.xpath('//*[@id="js-blogger-history-awemes"]/tr/td[2]/div/text()[2]')
        comment_count = video_html.xpath('//*[@id="js-blogger-history-awemes"]/tr/td[2]/div/text()[3]')
        share_count = video_html.xpath('//*[@id="js-blogger-history-awemes"]/tr/td[2]/div/text()[4]')
        for i in range(len(video_like)):
            KOL_video['title'] = title[i]
            KOL_video['video_like'] = video_like[i]
            KOL_video['comment_count'] = comment_count[i]
            KOL_video['share_count'] = share_count[i]
            print('KOL_data是{}'.format(KOL_video))

        target_url = detail_live_url.format(id=id_list[item], timestamp=timestamp_list[0],
                                            signature=signature_list[item])

        await page.goto(target_url)
        await page.waitFor(10000)
        content = await page.content()
        # print(content)
        html = etree.HTML(content)
        # print(html)
        # TODO 关注 链接
        follow = re.findall(' <a href="(.*)">', content)
        print('关注' + follow[0])
        # TODO 粉丝数
        total_fans = html.xpath('//*[@id="bloggerDetail-Div"]/div[1]/div/div[2]/div[2]/div[2]/div[1]/span/text()')
        # 总点赞
        like = html.xpath('//*[@id="bloggerDetail-Div"]/div[1]/div/div[2]/div[2]/div[4]/div[1]/span/text()')
        KOL_data['total_like'] = like[0]
        # 平均点赞
        average_like = html.xpath('//*[@id="bloggerDetail-Div"]/div[1]/div/div[2]/div[2]/div[4]/div[2]/span/text()')
        KOL_data['average_live'] = average_like[0]
        # 集均点赞90天内点赞数/视频数
        average_like_video = html.xpath(
            '//*[@id="bloggerDetail-Div"]/div[1]/div/div[2]/div[2]/div[5]/div[1]/span/text()')
        KOL_data['average_live_video'] = average_like_video[0]
        # 集均分享90天内分享视频数/视频数
        average_share_video = html.xpath(
            '//*[@id="bloggerDetail-Div"]/div[1]/div/div[2]/div[2]/div[5]/div[2]/span/text()')
        KOL_data['average_share_video'] = average_share_video[0]
        fans = html.xpath('//*[@id="bloggerDetail-Div"]/div[1]/div/div[2]/div[2]/div[2]/div[1]/span/text()')
        nickname = re.findall(r' data-nickname=(.*)data-bloggerid=', content)
        douyin_num = re.findall('抖音号：<span>(.*?)</span>', content)
        area = re.findall('地区：<span>(.*?)</span>', content)
        sex = html.xpath('//*[@id="bloggerDetail-Div"]/div[1]/div/div[1]/div/div[1]/div[2]/ul/li[2]/span[1]/text()')
        sort = re.findall('分类：<span class="bloggerTag.*?">(.*?)</span>', content)
        sign = html.xpath('//*[@id="bloggerDetail-Div"]/div[1]/div/div[1]/div/div[3]/span/text()')
        age = re.findall('年龄：<span>(.*?)</span>', content)
        if sex == []:
            first_page_data['sex'] = ''
        elif area == []:
            first_page_data['area'] = ''
        elif sort == []:
            first_page_data['sort'] = ''
        elif age == []:
            first_page_data['age'] = ''
        else:
            first_page_data['sex'] = sex[0]
            first_page_data['area'] = area[0]
            first_page_data['sort'] = sort[0]
            first_page_data['age'] = age[0]

        first_page_data['sign'] = sign[0]
        first_page_data['nickname'] = nickname[0]
        first_page_data['douyin_num'] = douyin_num[0]
        first_page_data['fans'] = fans[0]
        # TODO 作品数
        video_count = html.xpath('//*[@id="bloggerDetail-Div"]/div[1]/div/div[2]/div[2]/div[2]/div[2]/span/text()')
        first_page_data['video_count'] = video_count[0]
        print(first_page_data)

        await parse_live_page(page=page, KOL_live=KOL_live, uid=id_list[item])
        # live_total_sales=live_html.xpath('//*[@id="zb-record"]/div/div/div[1]/div[1]/div[2]/div[3]/ul/li[6]/span/text()')
        # live_data['live_total_sales']=live_total_sales[0]

        await page.waitFor(5000)
        await page.click('#js-tab_options > li:nth-child(7) > a')
        await page.waitFor(3000)
        fan_cotent = await page.content()
        re_total_fans = re.findall(r'var liveFansClub7 =(.*);', fan_cotent)
        total_fans = re_total_fans[-1]
        # TODO 粉丝团人数
        total_fans_y = total_fans['y']

    # live_content=await page.content()
    # live_times7=re.findall()
    # live_hour=re.findall()
    # live_people=re.findall()
    # live_goods=re.findall()
    # live_sales=re.findall()
    # live_total=re.findall()

    # await page.goBack()


event = asyncio.get_event_loop()
event.run_until_complete(test())
