"""
猫眼电影top100抓取（电影名称、主演、上映时间）
"""
# import requests
# import re
# import time
# import random

import re
import csv
import time
import random
import requests
import traceback
import pymysql
import pymongo


"""
sql 表创建

mysql -uroot -p
create database maoyandb charset utf8;
use maoyandb;
create table maoyantab(
name varchar(100),
star varchar(300),
time varchar(100)
)charset=utf8;
"""

"""
robots.txt
User-agent: *
Disallow: /*?utm_source*
"""

class MaoyanSpider:
    def __init__(self):
        self.url='https://maoyan.com/board/4?offset={}'
        self.headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'}
        # 创建mysql数据库连接+游标对象
        self.db = pymysql.connect('localhost', 'root', '123456', 'maoyandb', charset='utf8')
        self.cur = self.db.cursor()
        # 打开文件，初始化写入对象[在*inux下运行是utf8，而window下是国标GBK]
        self.f = open('maoyan.csv','w',newline='')

    def get_html(self,url):
        html=requests.get(url=url,headers=self.headers).content.decode('utf8')
        # html=requests.get(url=url,headers=self.headers).content.decode('utf8')
        # 直接调用解析函数
        self.parse_html(html)

    def parse_html(self,html):
        """解析提取数据"""
        regex = '<div class="movie-item-info">.*?title="(.*?)".*?<p class="star">(.*?)</p>.*?<p class="releasetime">(.*?)</p>'
        pattern = re.compile(regex,re.S)
        r_list = pattern.findall(html)
        # r_list: [('活着','牛犇','2000-01-01'),(),(),...,()]
        # 调用cvs保存
        # self.save_html(r_list)
        # 调用sql保存
        self.save_maoyandb(r_list)

    def save_maoyandb(self,r_list):
        """存入数据库"""
        ins = 'insert into maoyantab values(%s,%s,%s)'
        for r in r_list:
            li = [
                r[0].strip(),
                r[1].strip(),
                r[2].strip()
            ]
            self.cur.execute(ins,li)
            # 提交到数据库
            self.db.commit()
            print(li)

    def save_html(self,r_list):
        """数据处理函数"""
        item = {}
        for r in r_list:
            item['name'] = r[0].strip()
            item['star'] = r[1].strip()
            item['time'] = r[2].strip()
            print(item)

            try:
                with open('./cateye.csv', 'a', encoding='utf_8_sig', newline='') as fp:
                    # 'a'为追加模式（添加）
                    # utf_8_sig格式导出csv不乱码
                    fieldnames = ['name', 'star', 'time']
                    writer = csv.DictWriter(fp, fieldnames)
                    writer.writerow(item)
            except Exception:
                print(traceback.print_exc())  # 代替print e 来输出详细的异常信息



    def run(self):
        """程序启动函数"""
        for offset in range(0,91,10):
            url = self.url.format(offset)
            self.get_html(url=url)
            # 控制数据抓取频率：uniform（）生成制定范围内的浮点数
            time.sleep(random.uniform(2,5))

        # 执行数据库操作后在启动函数关闭
        self.cur.close()
        self.db.close()

if __name__ == '__main__':
    spider = MaoyanSpider()
    spider.run()
















