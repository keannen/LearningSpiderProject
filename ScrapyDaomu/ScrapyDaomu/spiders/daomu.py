import scrapy
from ..items import ScrapydaomuItem
import os

class DaomuSpider(scrapy.Spider):
    name = 'daomu'
    allowed_domains = ['www.daomubiji.com']
    start_urls = ['http://www.daomubiji.com/']

    def parse(self, response):
        """
        一级页面解析函数：提取标题、链接，并把大连接交给调度器入队列
        """
        a_list = response.xpath('//li[contains(@id,"menu-item-20")]/a')
        for a in a_list:
            item = ScrapydaomuItem()  # 实例化item列表
            parent_title = a.xpath('./text()').get()
            parent_url = a.xpath('./@href').get()
            item['directory'] = './novel/{}/'.format(parent_title)
            # 创建对应文件夹
            if not os.path.exists(item['directory']):
                os.makedirs(item['directory'])
            # 交给调度器入队列
            yield scrapy.Request(url=parent_url, meta={'meta_1': item}, callback=self.detail_page)

    # 返回11个response,调用该函数
    def detail_page(self, response):
        """
        二级页面解析函数：提取小标题、小链接
        """
        # 接收item
        meta_1 = response.meta['meta_1']
        art_list = response.xpath('//article')
        for art in art_list:
            # 只要有继续交往调度器的请求，就必须新建item对象
            item = ScrapydaomuItem()
            item['son_title'] = art.xpath('./a/text()').get()
            son_url = art.xpath('./a/@href').get()
            item['directory'] = meta_1['directory']
            # 再次交给调度器入队列
            yield scrapy.Request(url=son_url, meta={'item': item}, callback=self.get_content)

    # 盗墓笔记1: 传过来了75个response
    # 盗墓笔记2: 传过来了 n 个response
    # ....

    def get_content(self,response):
        """三级页面解析函数：提取具体小说内容"""
        item = response.meta['item']
        # content_list: ['段落1','段落2','段落3',...]
        content_list = response.xpath('//article[@class="article-content"]/p/text()').extract()
        item['content'] = '\n'.join(content_list)

        # 至此,一条item数据全部提取完成
        yield item