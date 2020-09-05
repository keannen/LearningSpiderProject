# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapytencentItem(scrapy.Item):
    # define the fields for your item here like:
    # 此处写哪些字段,标准为你的管道文件 pipelines.py 中你需要处理哪些数据
    # 名称 + 类别 + 职责 + 要求 + 地址 + 时间
    job_name = scrapy.Field()
    job_type = scrapy.Field()
    job_duty = scrapy.Field()
    job_require = scrapy.Field()
    job_add = scrapy.Field()
    job_time = scrapy.Field()
