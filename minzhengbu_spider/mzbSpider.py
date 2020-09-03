"""
抓取民政部最新月份行政区划代码
知识点:
    driver.switch_to.window()
"""
from selenium import webdriver
import time
import redis
from hashlib import md5
import sys

class MzbSpider:
    def __init__(self):
        self.url = 'http://www.mca.gov.cn/article/sj/xzqh/2020/'
        # 设置无界面模式
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=self.options)
        # 打开网站
        self.driver.get(url=self.url)
        # 连接redis
        self.r = redis.Redis(host='localhost', port=6379, db=0)

    def md5_url(self, url):
        """md5加密函数"""
        s = md5()
        s.update(url.encode())

        return s.hexdigest()

    def parse_html(self):
        # 找到最新月份的a节点
        newest_node = self.driver.find_element_by_xpath('//*[@id="list_content"]/div[2]/div/ul/table/tbody/tr[2]/td[2]/a')
        href = newest_node.get_attribute('href')
        finger = self.md5_url(url=href)
        if self.r.sadd('mzb:spiders', finger) == 1:
            newest_node.click()
            # 休眠一下,保证元素加载完全
            time.sleep(2)
            # 切换句柄
            all_handles = self.driver.window_handles
            self.driver.switch_to.window(all_handles[1])
            # 开始提取数据
            self.get_data()
        else:
            sys.exit('更新完成')

    def get_data(self):
        """二级页面解析函数:提取具体数据"""
        tr_list = self.driver.find_elements_by_xpath('//tr[@height="19"]')
        for tr in tr_list:
            item = {}
            item['name'] = tr.find_element_by_xpath('./td[3]').text.strip()
            item['code'] = tr.find_element_by_xpath('./td[2]').text.strip()
            print(item)

    def run(self):
        self.parse_html()
        self.driver.quit()

if __name__ == '__main__':
    spider = MzbSpider()
    spider.run()



































