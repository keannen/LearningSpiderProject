"""
    小米应用商店应用信息数据抓取
    1. 应用名称
    2. 应用链接
    3. 应用类别
"""
import requests, json, time, random, re, pymongo, csv
from fake_useragent import UserAgent


class XiaomiSpider:
    def __init__(self):
        self.url = 'http://app.mi.com/categotyAllListApi?page={}&categoryId={}&pageSize=30'
        # 三个对象
        self.conn = pymongo.MongoClient('localhost', 27017)
        self.db = self.conn['xiaomidb']
        self.myset = self.db['xiaomiset']
        # 计数
        self.num = 0

    def get_html(self, url):
        """请求功能函数"""
        headers = {'User-Agent':UserAgent().random}
        html = requests.get(url=url, headers=headers).text
        time.sleep(random.uniform(1,2))

        return html

    def parse_html(self, url):
        """爬虫程序从此开始"""
        html = self.get_html(url=url)
        html = json.loads(html)

        for one_app_dict in html['data']:
            item = {}
            item['name'] = one_app_dict['displayName']
            item['type'] = one_app_dict['level1CategoryName']
            item['link'] = 'http://app.mi.com/details?id=' + one_app_dict['packageName']
            print(item)
            # 数据存入mongdb数据库中
            self.myset.insert_one(item)

        L = []
        with open('xiaomiapp.csv', 'a', newline='') as f:
            # 初始化写入对象,注意参数f不能忘
            writer = csv.writer(f)
            for i in item:
                t = (
                    i[0].strip(),
                    i[1].strip(),
                    i[2].strip()
                )
                self.num += 1
                L.append(t)
            # writerow()参数为列表
            writer.writerows(L)
            print(L)

    # def save_csv(self,item):
    #     L = []
    #     with open('xiaomiapp.csv', 'a', newline='') as f:
    #         # 初始化写入对象,注意参数f不能忘
    #         writer = csv.writer(f)
    #         for i in item:
    #             t = (
    #
    #             )

    def get_total_page(self, one_id):
        """获取某个类别下的总页数"""
        # 向这个类别下的第一页发请求,提取count的值
        html = self.get_html(url=self.url.format(0, one_id))
        html = json.loads(html)
        count = html['count']
        # 计算总页数
        total_page = count // 30 if count % 30 == 0 else count // 30 + 1

        return total_page

    def get_all_id_list(self):
        """所有类别的id的值"""
        index_url = 'http://app.mi.com/'
        index_html = self.get_html(url=index_url)
        regex = '<li><a  href="/category/(.*?)">'
        pattern = re.compile(regex, re.S)
        all_id_list = pattern.findall(index_html)

        return all_id_list


    def run(self):
        # 获取某个类别下的总页数
        all_id_list = self.get_all_id_list()
        print(all_id_list)
        for one_id in all_id_list:
            total_page = self.get_total_page(one_id)
            print(total_page)
            for page in range(total_page):
                page_url = self.url.format(page, one_id)
                self.parse_html(url=page_url)
                # 控制数据抓取的频率
                time.sleep(random.randint(1, 2))

if __name__ == '__main__':
    spider = XiaomiSpider()
    spider.run()