# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class WyyxPipeline(object):
    def process_item(self, item, spider):
        # print(dict(item))
        return item

"""
pipelines.py处理数据
1、mysql数据库建库建表
create database wyyxdb charset utf8;
use beautytab;
create table beautytab(
goods_url varchar(200),
goods_title varchar(100),
goods_specifications_price varchar(100),
goods_evaluation varchar(100)
)charset=utf8;
"""
# 存入mysql
import pymysql
from .settings import *


class WyyxMysqlPipeline(object):
    def open_spider(self, spider):
        # 爬虫项目启动时 只执行一次 一般用于数据库连接
        self.db = pymysql.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PWD, MYSQL_DB, charset=CHARSET)
        self.cur = self.db.cursor()
        self.ins = 'insert into wyyxtab values(%s,%s,%s,%s,%s)'

    def process_item(self, item, spider):
        li = [
            item['goods_url'],  # 商品url
            item['goods_title'],  # 商品标题
            item['goods_specifications_price'],  # 商品规格 价格
            item['goods_details'],  # 商品详情
            item['goods_evaluation'],  # 商品评论
            ]
        self.cur.execute(self.ins, li)
        self.db.commit()

        return item

    def close_spider(self, spider):
        # 爬虫项目结束时 只执行一次 一般用于数据库断开
        self.cur.close()
        self.db.close()

#存入mongodb
import pymongo
class WyyxMongoPipeline(object):

    def open_spider(self,spider):
        self.conn=pymongo.MongoClient(MONGO_HOST,MONGO_PORT)
        self.db=self.conn[MONGO_DB]
        self.myset=self.db[MONGO_SET]

    def process_item(self, item, spider):
        self.myset.insert_one(dict(item))
        return item



