"""
肯德基餐厅门店信息抓取（POST请求练习,非多线程）
    1.1) URL地址: http://www.kfc.com.cn/kfccda/storelist/index.aspx
    1.2) 所抓数据: 餐厅编号、餐厅名称、餐厅地址、城市
    1.3) 数据存储: 保存到本地的json文件中,kfc.json
    1.4) 程序运行效果：
         请输入城市名称：北京
         把北京的所有肯德基门店的信息保存到json文件
"""
import requests
import random
import time
from fake_useragent import UserAgent


class KFCinfoSpider:
    def __init__(self):
        self.post_url = 'http://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=cname'
        self.city_name = input('请输入城市名称：')

    # 获取门店总页数
    def get_total_page(self):
        data = {
            'cname': self.city_name,
            'pid': '',
            'pageIndex': '1',
            'pageSize': '10',
        }
        headers = {'User-Agent': UserAgent().random}
        html = requests.post(url=self.post_url, headers=headers, data=data).json()
        count = html['Table'][0]['rowcount']
        total_page = count // 10 if count % 10 == 0 else count // 10 + 1
        return total_page

    # 获取
    def get_html(self):
        total_page = self.get_total_page()
        for page in range(1,total_page+1):
            data = {
                'cname':self.city_name,
                'pid':'',
                'pageIndex':str(page),
                'pageSize':'10',
            }
            headers = {'User-Agent':UserAgent().random}
            html = requests.post(url=self.post_url,headers=headers,data=data).json()
            for one_shop_dict in html['Table1']:
                item = {}
                item['row_num'] = one_shop_dict['rownum']
                item['store_name'] = one_shop_dict['storeName']
                item['province_name'] = one_shop_dict['provinceName']
                item['city_name'] = one_shop_dict['cityName']
                item['address_detail'] = one_shop_dict['addressDetail']
                print(item)
            #控制抓取的频率
            time.sleep(random.uniform(3,5))

    def run(self):
        self.get_html()

if __name__ == '__main__':
    spider = KFCinfoSpider()
    spider.run()

