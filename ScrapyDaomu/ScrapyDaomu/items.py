# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ScrapydaomuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # items 需要处理的数据：文件名、路径
    # 文件名：小标题名称  son_title: 七星鲁王 第一章 血尸
    son_title = scrapy.Field()
    directory = scrapy.Field()
    content = scrapy.Field()
