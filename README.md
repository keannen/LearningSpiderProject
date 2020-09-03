# LearningSpiderProject
LearningSpiderProject：2020/7/11

#  `警告：本教程仅用作学习交流，请勿用作商业盈利，违者后果自负！如本文有侵犯任何组织集团公司的隐私或利益，请告知留言删除！！！`

# 爬虫项目：
###   知识架构

- 服务端
  - 页面的结果是由服务器渲染后返回的，有效信息包含在请求的html页面里。
  - 爬虫实现
    - urllib	python自带的原生底层库
    - urllib3    相比urllib增加了许多新特性
    - pycurl    libcurl的python实现
    - hyper     支持http2的新特性
    - requests    应用最广泛的http请求库
    - grab    基于urllib3和PyQuery封装

- 客户端
  - 页面的主要内容有JavaScript渲染而成，真实的数据是通过Ajax接口等形式获取的，比如淘宝。天猫、微博手机版等站点
  - 爬虫实现
    - 寻找Ajax接口
    - 模拟浏览器执行    【Selenium、Pyppeteer、PhantomJS、Splinter、Spynner、Splash、request-html】
    - 提取JavaScripts数据
    - 执行JavaScript    【Selenium、PyExecJS、PyV8、js2py】

###  爬虫项目

- QQ邮箱登录（反爬技术难点：异步嵌套iframe的破解）【selenium、lxml解析】

- scrapy百度【scrapy框架】

- 猫眼电影 【request请求、UserAgent伪造、re解析、mysql导入、csv(导出excel)、mongodb导入】

- 豆瓣电影全站抓取（反爬技术难点：js抓包获取对应的json文件）【request请求、re解析、UserAgent伪造、json解析、Threading多线程、Queue队列】

- kfc门店信息（反爬技术难点：ajax异步访问破解通过Chrome抓包获取json文件）【request请求、UserAgent伪造、json解析】附带json测试解析Demo

- 快代理（实时获取免费ip即爬即用）【request请求、UserAgent伪造、lxml解析、mysql导入】

- 拉钩网岗位（

  - 反爬技术难点：
    - ajax异步访问获取json
    - url重定向（通过request.session获取和清除cookies信息）
    - json链接只能访问一次，之后就无效
    - ip限制（阿布云代理）
  - 【request请求、UserAgent伪造、session保持连接、阿布云ip代理、cookies清除与获取、json解析、multiprocessing多进程抓取、flask框架、echarts可视化】

- 链家【request请求、UserAgent伪造、lxml解析、mysql导入、csv(导出excel)】

- 民政局最新月份行政区划代码 （反爬技术难点：假链接嵌套，一切以响应内容为主,响应内容中没有 tbody 节点，从二级页面中提取真实返回数据的链接 - 即:URL地址跳转后的链接）

  - selenium版本【selenium、md5指纹加密、redis入库去重】
  - request版本【requests请求、lxml解析、re解析】

- pyppeteer学习

- Selenium学习

- 小米app目录全站爬【request请求、UserAgent伪造、re解析、csv(导出excel)、mongodb导入】

- 有道翻译

  - 经典js逆向:通过伪造salt、sign、ts获取翻译后的信息
  - selenium简单版通过浏览器的手机版抓取信息
  - 【requests请求、json解析】

  
