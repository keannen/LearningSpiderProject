# -*- coding: utf-8 -*-
import scrapy


class ScrapymaoyanSpider(scrapy.Spider):
    name = 'scrapymaoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/board/4']

    def parse(self, response):
        dd_list = response.xpath('')
        for dd in dd_list:
            item = ScrapymaoyanSpiderItem()
        pass
