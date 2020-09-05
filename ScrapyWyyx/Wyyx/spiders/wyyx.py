# -*- coding: utf-8 -*-
import scrapy
import json
import re
import time
from urllib import parse
from ..items import WyyxItem

class WyyxSpider(scrapy.Spider):
    name = 'wyyx'
    allowed_domains = ['you.163.com']

    def start_requests(self):
        user_input = '美妆'
        url='https://you.163.com/xhr/search/search.json?&page=1&size=10&keyword={}'.format(parse.quote(user_input))
        yield scrapy.Request(url=url,meta={'user_input': user_input},callback=self.get_goods_page)

    def get_goods_page(self,response):
        user_input=response.meta['user_input']
        response_json=json.loads(response.text)
        goods_total=response_json['data']['directly']['searcherResult']['pagination']['total']#获取商品总计数
        goods_total=goods_total//40 if goods_total%40==0 else goods_total//40+1
        for page in range(1,goods_total+1):
            url='https://you.163.com/xhr/search/search.json?&page={}&size=40&keyword={}'.format(page,parse.quote(user_input))
            # print(goods_total,url)
            yield scrapy.Request(url=url,callback=self.get_goods_url)
            # time.sleep(2)


    def get_goods_url(self,response):
        # item=WyyxItem()
        response_json = json.loads(response.text)
        goods_url = response_json['data']['directly']['searcherResult']['result'] # 获取商品id
        for id in goods_url:
            # item['goods_url']
            url='http://you.163.com/item/detail?id={}'.format(id['id'])#拼接url
            print(url)
            yield scrapy.Request(url=url,meta={'id':id['id']},callback=self.get_goods_info)
            # time.sleep(2)




    def get_goods_info(self,response):
        id=response.meta['id']
        item = WyyxItem()
        re_parse=re.compile('var JSON_DATA_FROMFTL = (.*?"giftcardRealNameAuthAmount":1000.*?);',re.S)
        response_re=re_parse.findall(response.text)
        response_json=json.loads(str(response_re[0]).replace("'",'"'))

        goods_all_info=response_json['item']#商品全部信息
        goods_comments=response_json#商品评论信息

        goods_title=''#商品标题
        goods_specifications_price=''#商品规格 价格
        goods_details=''#商品详情
        goods_evaluation=''#商品评论

        goods_title+=goods_all_info['name']#商品标题
        # print(goods_title)

        for info in goods_all_info['attrList']:#商品详情
            goods_details+='{}:{}\n'.format(info['attrName'],info['attrValue'])
        # print(goods_details)

        for a in goods_all_info['skuMap']:#商品规格与商品价格
            goods_specifications_price+='￥{} - {}\n'.format(goods_all_info['skuMap'][a]['calcPrice'],goods_all_info['skuMap'][a]['specList'][0]['specValue'])#商品规格
        # print(goods_specifications_price)

        goods_evaluation+='{}条评论,好评率{}'.format(goods_comments['commentCount'],goods_comments['commentGoodRates'])

        item['goods_url'] = 'http://you.163.com/item/detail?id={}'.format(id)#拼接url
        item['goods_title'] =goods_title#商品标题
        item['goods_specifications_price'] =goods_specifications_price#商品规格
        item['goods_details'] =goods_details#商品详情
        item['goods_evaluation'] =goods_evaluation#商品详情

        # print(item)
        yield item
