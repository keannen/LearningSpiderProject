# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
import requests
import json
from ..items import ScrapytencentItem

class ScrapytencentSpider(scrapy.Spider):
    name = 'scrapytencent'
    allowed_domains = ['careers.tencent.com']
    one_url = 'https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1566266592644&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword={}&pageIndex={}&pageSize=10&language=zh-cn&area=cn'
    two_url = 'https://careers.tencent.com/tencentcareer/api/post/ByPostId?timestamp=1566266695175&postId={}&language=zh-cn'
    keyword = input('请输入关键字:')
    keyword = parse.quote(keyword)
    start_urls = [one_url.format(keyword, 1)]


    # 将所有一级页面URL地址交给调度器入队列
    def parse(self, response):
        total = self.get_total()
        for page_index in range(1, total+1):
            url = self.one_url.format(self.keyword, page_index)
            yield scrapy.Request(url=url, callback=self.parse_one_page)


    # 获取keyword类别下的职位总页数
    def get_total(self):
        url = self.one_url.format(self.keyword, 1)
        headers = {'User-Agent':'Mozilla/5.0'}
        html = requests.get(url=url, headers=headers).json()
        cou = html['Data']['Count']
        total = cou//10 if cou%10==0 else cou//10 + 1

        return total

    # 一级页面解析函数：提取postid, 并拼接二级页面URL地址, 交给调度器入队列
    def parse_one_page(self,response):
        # response.text : 获取响应内容,字符串
        html = json.loads(response.text)
        for one_job in html['Data']['Posts']:
            post_id = one_job['PostId']
            # 每页拼接10个职位的详情页链接
            two_url = self.two_url.format(post_id)
            yield scrapy.Request(url=two_url, callback=self.parse_two_page)

    # 二级页面解析函数：提取职位具体数据
    def parse_two_page(self,response):
        html = json.loads(response.text)
        item = ScrapytencentItem()
        item['job_name'] = html['Data']['RecruitPostName']
        item['job_type'] = html['Data']['CategoryName']
        item['job_duty'] = html['Data']['Responsibility']
        item['job_require'] = html['Data']['Requirement']
        item['job_add'] = html['Data']['LocationName']
        item['job_time'] = html['Data']['LastUpdateTime']

        yield item