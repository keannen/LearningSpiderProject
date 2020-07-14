"""
    快代理高匿代理,并测试,建立代理Ip池
    把可用的代理ip存放到mysql数据库中
"""

"""
mysql -uroot -p
create database proxydb charset utf8;
use proxydb;
create table proxytab(
ip varchar(100),
port varchar(50)
)charset=utf8;
"""
import requests
from lxml import etree
import time
import pymysql
from fake_useragent import UserAgent
import random

class KuaiProxyPool:
    def __init__(self):
        self.url = 'https://www.kuaidaili.com/free/inha/{}/'
        self.test_url = 'http://httpbin.org/get'
        self.db = pymysql.connect('localhost', 'root', '123456', 'proxydb', charset='utf8')
        self.cur = self.db.cursor()

    def get_html(self, url):
        """功能函数"""
        headers = {'User-Agent':UserAgent().random}
        html = requests.get(url=url, headers=headers).text

        return html

    def get_proxy(self, url):
        html = self.get_html(url=url)
        p = etree.HTML(html)
        tr_list = p.xpath('//table/tbody/tr')
        for tr in tr_list:
            ip = tr.xpath('./td[1]/text()')[0].strip()
            port = tr.xpath('./td[2]/text()')[0].strip()
            # 测试此ip和port是否可用
            self.test_proxy(ip, port)

    def test_proxy(self, ip, port):
        """测试ip是否可用"""
        proxies = {
            'http' : 'http://{}:{}'.format(ip, port),
            'https': 'https://{}:{}'.format(ip, port)
        }
        headers = {'User-Agent':UserAgent().random}
        try:
            resp = requests.get(url=self.test_url, headers=headers, proxies=proxies, timeout=3)
            if resp.status_code == 200:
                print(ip, port, '可用')
                # 把可用的ip存入到数据库
                self.insert_mysql(ip, port)
            else:
                print(ip, port, '不可用')
        except Exception as e:
            print(ip, port, '不可用')

    def insert_mysql(self, ip, port):
        """把ip和port存入数据库"""
        ins = 'insert into proxytab(ip,port) values(%s,%s)'
        self.cur.execute(ins, [ip, port])
        self.db.commit()

    def run(self):
        for i in range(1, 1001):
            page_url = self.url.format(i)
            self.get_proxy(url=page_url)
            time.sleep(random.randint(1,3))

if __name__ == '__main__':
    spider = KuaiProxyPool()
    spider.run()



