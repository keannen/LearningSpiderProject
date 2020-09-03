# ## request爬取京东
"""
mysql -uroot -proot
create database jddb charset utf8;
use jddb;
create table jd_beauty_tab(
name varchar(200),
price varchar(50),
shop varchar(50),
url varchar(200)
)charset=utf8;
"""
from concurrent.futures.thread import ThreadPoolExecutor

import sys

from lxml import etree
from hashlib import md5
import pymysql
import redis
import requests
import time,random
from fake_useragent import UserAgent


class JdSpider(object):

    def __init__(self):
        """初始化"""
        self.url = 'https://search.jd.com/Search?keyword={}&page={}'
        # 线程池
        self.jd_pool = ThreadPoolExecutor(max_workers=10)  # 线程池. 数量自己定义
        # 连接mysql
        self.db = pymysql.connect('localhost', 'root', '123456', 'jddb', charset='utf8')
        self.cursor = self.db.cursor()
        # 连接redis
        self.res = redis.Redis(host='localhost', port=6379, password='123456', db=0, decode_responses=True)
        # 创建报错日志
        self.jd_beauty_log_info = open('jd_beauty_log_info.txt', 'a', encoding='utf-8')

    def get_html(self, url):
        """
        爬取京东页面
        :param url:
        :return:
        """
        try:
            headers = {'User-Agent' : UserAgent().random}
            response = requests.get(url=url, headers=headers).text
            self.parse_html(response)
        except:
            self.jd_beauty_log_info.write(f'请求超时报错,{url}\n')
            print(f'请求超时报错,{url}\n')

    def md5_url(self, url):
        """md5加密"""
        s = md5()
        s.update(url.encode())
        return s.hexdigest()

    def parse_html(self, response):
        """
        解析页面将商品url通过指纹加密后增量爬取
        :param response: 网页响应
        :return:
        """
        parse = etree.HTML(response)
        good_info = {}
        url_list = parse.xpath('//div[@class="p-name p-name-type-2"]/a/@href')
        # good_title = parse.xpath('.//ul/li//div[@class="p-name p-name-type-2"]//em/text()')
        good_title = parse.xpath('.//div[@class="p-name p-name-type-2"]/a/em')
        good_price = parse.xpath('.//ul/li//div[@class="p-price"]/strong/i/text()')
        good_shop = parse.xpath('.//ul/li//div[@class="p-shop"]//a/text()')

        for i in range(len(url_list)):
            good_info['title'] = good_title[i].strip()
            good_info['price'] = good_price[i].strip()
            good_info['shop'] = good_shop[i].strip()
            good_info['url'] = url_list[i][2:].strip()
            print(good_title['title'])

            finger = self.md5_url(good_info['url'])
            # 返回值为1: 之前没有抓过
            if self.res.sadd('jd:face', finger) == 1 and len(good_info['title'])>=2 :
                # print('parse_html_good_info', good_info)
                self.save_as_mysql(good_info)
            else:

                print('数据已存入')
                # self.jd_beauty_log_info.write(f'数据已存入,{good_info}\n')
        # 控制数据抓取的频率,uniform生成浮点数
        time.sleep(random.uniform(1, 2))

    def save_as_mysql(self, good_info):
        """
        存入数据库
        :param good_info: 标题、价格、商店名称、商品链接
        :return: None
        """
        insert = 'insert jd_beauty_tab values(%s,%s,%s,%s)'
        info = [
            good_info['title'],
            good_info['price'],
            good_info['shop'],
            good_info['url']
        ]
        self.cursor.execute(insert, info)
        # print('info', info)
        self.db.commit()

    def run(self):
        """
        启动函数
        :return: None
        """
        try:
            start_time = time.time()
            key_list = ["洁面","化妆水","精华","乳液","面霜","眼霜","面膜","护肤套装","卸妆","防晒","BB霜","粉饼","眼影","睫毛膏","唇彩","腮红","彩妆套装"]
            # keyword = '洁面'
            for keyword in range(len(key_list)):
                for page in range(1, 101):
                    # 循环获取每一页的url
                    url = self.url.format(key_list[keyword], page)
                    self.get_html(url=url)
                    print('正在抓取第{}页'.format(page))
                    self.jd_beauty_log_info.write(f'第{page}页已抓取成功\n')
                print("{}类抓取完毕".format(key_list[keyword]))
                self.jd_beauty_log_info.write(f'{key_list[keyword]}类已抓取成功\n')

            end_time = time.time()
            seconds = end_time - start_time
            m, s = divmod(seconds, 60)
            h, m = divmod(m, 60)
            print("程序执行时间：%d:%02d:%02d" % (h, m, s))
        finally:
            self.cursor.close()
            self.db.close()


if __name__ == '__main__':
    spider = JdSpider()
    spider.run()