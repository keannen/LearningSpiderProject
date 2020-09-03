import requests
import json
import random
import time
from queue import Queue
from threading import Thread,Lock
from fake_useragent import UserAgent

class DoubanThreadSpider:
    def __init__(self):
        self.url = 'https://movie.douban.com/j/chart/top_list?type=11&interval_id=100%3A90&action=&start={}&limit=20'
        # 定义队列和锁
        self.q = Queue()
        self.lock = Lock()

    # 请求功能函数：获取网页源码
    def get_html(self,url):
        headers = {'User-Agent':UserAgent().random}
        html = requests.get(url=url,headers=headers).text
        return html

    # 把所有要抓取的URL地址入队列
    def url_in(self):
        for page in range(1,21):
            start = (page - 1)*20
            page_url = self.url.format(start)
            # 入队列
            self.q.put(page_url)

    # 创建线程事件函数:请求＋解析＋数据处理
    def parse_html(self):
        if not self.q.empty():
            url = self.q.get()
            html = json.loads(self.get_html(url=url))
            for one_file_dict in html:
                item = {}
                item['rank'] = one_file_dict['rank']
                item['title'] = one_file_dict['title']
                item['score'] = one_file_dict['score']
                print(item)

    #  程序入口函数
    def run(self):
        # 先让ｕｒｌ入队列
        self.url_in()
        # 创建多线程
        t_list = []
        for i in range(2):
            t = Thread(target=self.parse_html)
            t_list.append()
            t.start()

        # 统一ｊｏｉｎ
        for t in t_list:
            t.join()

if __name__ == '__main__':
    start_time = time.time()
    spider = DoubanThreadSpider()
    spider.run()
    end_time = time.time()
    print('time:%.2f'%(end_time-start_time))