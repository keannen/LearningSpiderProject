# -*- coding: utf-8 -*-
import scrapy
from ..items import JdItem
from urllib import parse
import time
import re
import json


class JdSpider(scrapy.Spider):
    name = 'jd'
    # allowed_domains = ['www.jd.com']

    def start_requests(self):
        commodity_species = input('www.jd.com->输入你要爬取的商品类:')
        commodity_species = parse.quote(commodity_species)
        num = int(input('输入需要爬去的页数:'))

        for n in range(1,num+1):
            s = 30*n+1
            url ='https://search.jd.com/Search?keyword={}&page={}&s={}&click=0'.format(commodity_species,n,s)
            print('入队了',url)
            yield scrapy.Request(url=url,callback=self.parse_1)

    def parse_1(self, response):
        '''一级页面'''
        div_list = response.xpath('//div[@class="gl-i-wrap"]/div[@class="p-img"]')
        for div in div_list:
            item = JdItem()
            link = div.xpath('./a/@href').get() #获取2级页面链接
            item['commodity_id'] = re.findall('\d+',link)[0] #获取id
            item['price'] = response.xpath('//strong[@class="J_{}"]//i/text()'.format(item['commodity_id'])).get()
            two_url = 'https:'+ link #拼接二级页面
            time.sleep(1)
            yield scrapy.Request(url=two_url,meta={'item':item},callback=self.parse_2)


    def parse_2(self,response):
        '''二级页面'''
        item = response.meta['item']
        item['shop'] = response.xpath('//div[@id="crumb-wrap"]/div/div[2]/div[2]/div[1]/div/a/text()').get()
        item['commodity'] = response.xpath('//div[@class="item ellipsis"]/text()').get()

        # size_list = response.xpath('//div[@id="choose-attr-2"]//div[2]').get()
        # if not size_list:
        #     size_list = None
        # else:
        #     size = re.findall('data-value="(.*?)"', size_list)
        #     item['commodity_size'] = (',').join(size)
        # item['commodity_size'] = size_list

        item['shop_star'] = response.xpath('//div[@class="pop-score-summary"]/a//div[@class="star-gray"]/@title').get()
        item['commodity_score'] = response.xpath('//div[@class="score-parts"]/div[1]/span[2]/em/text()').get()
        item['logistics_score'] = response.xpath('//div[@class="score-parts"]/div[2]/span[2]/em/text()').get()
        item['after_sale_service'] = response.xpath('//div[@class="score-parts"]/div[3]/span[2]/em/text()').get()
        three_url ='https://club.jd.com/comment/productPageComments.action?productId={}&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'.format(item['commodity_id'])
        time.sleep(1)
        yield scrapy.Request(url=three_url,meta={'item':item},callback=self.parse_3)

    def parse_3(self,response):
        '''三级页面'''
        item = response.meta['item']
        data=json.loads(response.text)
        item['goodcount'] = data['productCommentSummary']['goodCount']
        item['poorcount'] = data['productCommentSummary']['poorCount']
        item['generalcount'] =data['productCommentSummary']['generalCount']
        time.sleep(1)
        yield item


