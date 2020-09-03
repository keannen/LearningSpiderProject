# ## request爬取京东
"""
mysql -uroot -proot
create database jddb charset utf8;
use jddb;
create table jdtab(
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
        self.res = redis.Redis(host='localhost', port=6379, password='123456', db=3, decode_responses=True)
        # 创建报错日志
        self.jdspider_log_info = open('jdspider_log_info.txt', 'a')

    def get_html(self, url):
        """
        爬取京东页面
        :param url:
        :return:
        """
        try:
            headers = {'User-Agent' : UserAgent().random}
            response = requests.get(url=url, headers=headers).text
            print("爬取的url",url)
            self.parse_html(response)
        except:
            self.jdspider_log_info.write(f'请求超时报错,{url}\n')
            print(f'请求超时报错,{url}\n')

    def md5_url(self, url):
        """md5加密"""
        s = md5()
        s.update(url.encode())
        return s.hexdigest()

    def parse_html(self, response):
        parse = etree.HTML(response)
        good_info = {}
        url_list = parse.xpath('//div[@class="p-name p-name-type-2"]/a/@href')
        good_title = parse.xpath('.//ul/li//div[@class="p-name p-name-type-2"]//em')
        # good_title = parse.xpath('.//div[@class="p-name p-name-type-2"]/a/text()')
        good_price = parse.xpath('.//ul/li//div[@class="p-price"]/strong/i/text()')
        good_shop = parse.xpath('.//ul/li//div[@class="p-shop"]//a/text()')

        for i in range(len(url_list)):
            good_info['title'] = good_title[i].strip()
            good_info['price'] = good_price[i].strip()
            good_info['shop'] = good_shop[i].strip()
            good_info['url'] = url_list[i][2:].strip()
            print('parse_html_good_info', good_info)
            self.save_as_mysql(good_info)
        # 控制数据抓取的频率,uniform生成浮点数
            time.sleep(random.uniform(1, 2))

    def save_as_mysql(self, good_info):
        insert = 'insert jdtab values(%s,%s,%s,%s)'
        info = [
            good_info['title'],
            good_info['price'],
            good_info['shop'],
            good_info['url']
        ]
        self.cursor.execute(insert, info)
        print('info', info)
        self.db.commit()

    def run(self):
        try:
            start_time = time.time()
            keyword = '洁面'
            for page in range(1, 3):
                # 循环获取每一页的url
                url = self.url.format(keyword, page)
                self.get_html(url=url)
                print('正在抓取第{}页'.format(page))
            end_time = time.time()
            print("程序执行时间：%.2f" % (end_time - start_time))
        finally:
            self.cursor.close()
            self.db.close()


if __name__ == '__main__':
    spider = JdSpider()
    spider.run()