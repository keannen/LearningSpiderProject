import scrapy


class ScrapybaiduSpider(scrapy.Spider):
    name = 'scrapybaidu'
    allowed_domains = ['www.baidu.com']
    start_urls = ['http://www.baidu.com/']

    def parse(self, response):
        r_list = response.xpath('/html/head/title/text()').extract()[0]
        print(r_list)
