# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# 管道1 : 从终端打印输出
class ScrapytencentPipeline(object):
    def process_item(self, item, spider):
        print(dict(item))
        return item

# 管道2 :存入mysql数据库
import pymysql
from .settings import *

class ScrapytencentMysqlPipline:
    def open_spider(self,spider):
        # 爬虫项目启动时,只执行一次,一般用于数据库连接
        self.db = pymysql.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PWD, MYSQL_DB, charset=CHARSET)
        self.cur = self.db.cursor()
        self.ins = 'insert into tencenttab values(%s,%s,%s,%s,%s,%s)'

    def process_item(self,item,spider):
        li = [
            item['job_name'],
            item['job_type'],
            item['job_duty'],
            item['job_require'],
            item['job_add'],
            item['job_time'],
        ]
        self.cur.execute(self.ins,li)
        self.db.commit()

        return item

    # 爬虫项目结束时, 只执行一次, 一般用于数据库断开
    def close_spider(self,spider):
        self.cur.close()
        self.db.close()

# 管道3 - MongoDB
import pymongo
class ScrapytencentMongoPipline:
    def open_spider(self,spider):
        self.conn = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
        self.db = self.conn[MONGO_DB]
        self.myset = self.db[MONGO_SET]

    def process_item(self,item,spider):
        self.myset.insert_one(dict(item))

        return item