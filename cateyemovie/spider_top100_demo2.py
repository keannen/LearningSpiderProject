import requests
import re
import time
import random


class MaoyanSpider(object):
    def __init__(self):
        self.url = 'https://maoyan.com/board/4?offset={}'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1'}
        self.i = 0

    def get_html(self, url):
        html = requests.get(url=url, headers=self.headers).text
        # 直接调用解析函数
        self.parse_html(html)

    def parse_html(self, html):
        """正则解析函数"""
        regex = '<div class="movie-item-info">.*?title="(.*?)".*?class="star">(.*?)</p>.*?releasetime">(.*?)</p>'
        pattern = re.compile(regex, re.S)
        # dd_list: [(),(),()]
        dd_list = pattern.findall(html)
        self.save_html(dd_list)

    def save_html(self, dd_list):
        """保存数据函数"""
        item = {}
        for dd in dd_list:
            item['name'] = dd[0].strip()
            item['star'] = dd[1].strip()[3:]
            item['time'] = dd[2].strip()[5:15]
            print(item)
            self.i += 1

    def run(self):
        for offset in range(0, 91, 10):
            url = self.url.format(offset)
            self.get_html(url)
            time.sleep(random.randint(3, 5))
        print('电影数量：', self.i)


if __name__ == '__main__':
    start_time = time.time()
    spider = MaoyanSpider()
    spider.run()
    end_time = time.time()
    print('执行时间:%.2f' % (end_time - start_time))