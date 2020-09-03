"""
requests + lxml 提取最新月份行政区划代码
"""
import requests
from lxml import etree
from fake_useragent import UserAgent
import re

class MzbSpider:
    def __init__(self):
        self.url = 'http://www.mca.gov.cn/article/sj/xzqh/2020/'

    def get_html(self, url):
        """请求功能函数"""
        headers = {'User-Agent':UserAgent().random}
        html = requests.get(url=url, headers=headers).text

        return html

    def parse_html(self):
        one_html = self.get_html(url=self.url)
        p = etree.HTML(one_html)
        # 坑1：一切以响应内容为主,响应内容中没有 tbody 节点
        href_list = p.xpath('//table/tr[2]/td[2]/a[1]/@href')
        two_url = 'http://www.mca.gov.cn' + href_list[0]
        two_html = self.get_html(url=two_url)
        # 从two_html中提取真实返回数据的链接 - 即:URL地址跳转后的链接
        self.get_real_url(two_html)

    def get_real_url(self, two_html):
        """获取真实返回数据的url地址"""
        regex = 'window.location.href="(.*?)"'
        pattern = re.compile(regex, re.S)
        real_url = pattern.findall(two_html)[0]
        # 提取具体的数据
        self.get_data(real_url)

    def get_data(self, real_url):
        """提取具体数据"""
        html = self.get_html(url=real_url)
        p = etree.HTML(html)
        tr_list = p.xpath('//tr[@height="19"]')
        for tr in tr_list:
            item = {}
            item['name'] = tr.xpath('./td[3]/text()')[0].strip()
            item['code'] = tr.xpath('./td[2]/text() | ./td[2]/span/text()')[0].strip()
            print(item)

    def run(self):
        self.parse_html()

if __name__ == '__main__':
    spider = MzbSpider()
    spider.run()














