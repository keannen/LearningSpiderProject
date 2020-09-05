# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from .settings import *
import pymysql

class JdPipeline(object):
    def process_item(self, item, spider):
        print(item)
        return item

#mysql
class JdMysqlPipeline:
    def open_spider(self,spider):
        self.db = pymysql.connect(MYSQL_HOST,MYSQL_USER,MYSQL_PWD,MYSQL_DB,charset=CHARSET)
        self.cur = self.db.cursor()
        self.ins = 'insert into jdtab values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        print('Mysql ok~~~~')

    def process_item(self,item,spider):
        li = [
            item['shop'],
            item['commodity_id'],
            item['commodity'],
            item['price'],
            # item['commodity_size'],
            item['shop_star'],
            item['commodity_score'],
            item['logistics_score'],
            item['after_sale_service'],
            item['goodcount'],
            item['generalcount'],
            item['poorcount'],
        ]
        self.cur.execute(self.ins,li)
        self.db.commit()
        return item


    def close_spider(self,spider):
        self.cur.close()
        self.db.close()

#mongo
import pymongo
class JdMongoPipeline:
    def open_spider(self,spider):
        self.conn = pymongo.MongoClient(MONGO_HOST,MONGO_PORT)
        self.db = self.conn[MONGO_DB]
        self.myset = self.db[MONGO_SET]
        print('Mongo ok~~~')

    def process_item(self, item, spider):
        self.myset.insert_one(dict(item))
        return item
