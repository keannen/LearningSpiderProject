#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Author : Johnny
# @Contact :  1306213653@qq.com
# @Time : 2020-09-04 14:02
# @File : jmyp_data_handle.py

import pandas as pd
import matplotlib.pyplot as plt
import pymongo
# matplotlib inline
# 连接mongodb数据库
client = pymongo.MongoClient("localhost")
# 连接数据库
db = client["jmypdb"]
# 数据表
jmyp = db["jmypdb"]
# 将mongodb中的数据读出
data = pd.DataFrame(list(jmyp.find()))
data.head()
# 保存为csv格式
data.to_csv('jmyp.csv', encoding="utf-8")
# 读取csv数据
df = pd.read_csv('jmyp.csv', low_memory=False, index_col=0)
# 查看数据大小(行列)
data.shape
# 查看数据行号
data.columns
# 找出所有满足字段的行
df1 = data.loc[:,["pid","title","price"]]
print(df1)