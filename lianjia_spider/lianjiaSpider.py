import csv

import requests
from lxml import etree
import time
import random
from fake_useragent import UserAgent

class LianjiaSpider(object):
    def __init__(self):
        self.url = 'https://bj.lianjia.com/ershoufang/pg{}/'
        # 打开文件
        self.f = open('Lianjia.csv', 'w', newline='')
        self.topnames = ['名称', '地址', '户型', '总面积/平米', '朝向', '装修', '楼层', '始于', '类型', '总价/万', '单价元/平米']
        self.writer = csv.writer(self.f)
        self.writer.writerow(self.topnames)


    def parse_html(self,url):
        headers = {'User-Agent':UserAgent().random}
        html = requests.get(url=url,headers=headers).content.decode('utf-8','ignore')
        self.get_data(html)


    def get_data(self,html):
        p = etree.HTML(html)
        # 基准xpath: [<element li at xxx>,<element li>]
        li_list = p.xpath('//ul[@class="sellListContent"]/li[@class="clear LOGVIEWDATA LOGCLICKDATA"]')
        # for遍历,依次提取每个房源信息,放到字典item中
        item = {}
        # self.writer.writerow('')
        for li in li_list:
            # 名称+区域
            name_list = li.xpath('.//div[@class="positionInfo"]/a[1]/text()')
            item['name'] = name_list[0].strip() if name_list else None
            address_list = li.xpath('.//div[@class="positionInfo"]/a[2]/text()')
            item['address'] = address_list[0].strip() if address_list else None
            # 户型+面积+方位+是否精装+楼层+年代+类型
            # h_list: ['']
            h_list = li.xpath('.//div[@class="houseInfo"]/text()')
            if h_list:
                info_list = h_list[0].split('|')
                if len(info_list) == 7:
                    item['model'] = info_list[0].strip()
                    item['area'] = info_list[1].strip()
                    item['direct'] = info_list[2].strip()
                    item['perfect'] = info_list[3].strip()
                    item['floor'] = info_list[4].strip()
                    item['year'] = info_list[5].strip()[:-2]
                    item['type'] = info_list[6].strip()
                else:
                    item['model'] = item['area'] = item['direct'] = item['perfect'] = item['floor'] = item['year'] = item['type'] = None
            else:
                item['model'] = item['area'] = item['direct'] = item['perfect'] = item['floor'] = item['year'] = item['type'] = None

            # 总价+单价
            total_list = li.xpath('.//div[@class="totalPrice"]/span/text()')
            item['total'] = total_list[0].strip() if total_list else None
            unit_list = li.xpath('.//div[@class="unitPrice"]/span/text()')
            item['unit'] = unit_list[0][2:-4].strip() if unit_list else None
            self.writer.writerow(item.values())
            print(item)

    def run(self):
        for pg in range(1,2):
            url = self.url.format(pg)
            self.parse_html(url)
            time.sleep(random.randint(3,5))

if __name__ == '__main__':
    spider = LianjiaSpider()
    spider.run()