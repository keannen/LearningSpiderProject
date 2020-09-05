# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WyyxItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    goods_url=scrapy.Field()#商品url
    goods_title=scrapy.Field()#商品标题
    goods_specifications_price=scrapy.Field()#商品规格 价格
    goods_details=scrapy.Field()#商品详情
    goods_evaluation=scrapy.Field()#商品评论






