# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class JdItem(scrapy.Item):
    # define the fields for your item here like:
    #一级页面
    #商品id
    commodity_id = scrapy.Field() #ok


    #二级页面
    #店名 商品 尺寸 价格
    shop = scrapy.Field() #ok
    commodity = scrapy.Field() #ok
    # commodity_size = scrapy.Field()
    price = scrapy.Field()
    #评分 商店星数
    shop_star = scrapy.Field()
    commodity_score = scrapy.Field()
    logistics_score = scrapy.Field()
    after_sale_service = scrapy.Field()

    #三级页面
    #好 中 差 评
    goodcount = scrapy.Field()
    generalcount = scrapy.Field()
    poorcount = scrapy.Field()

