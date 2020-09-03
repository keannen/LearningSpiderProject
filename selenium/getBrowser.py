#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@Author      : Joey
@fileName    : GetBrowser.py
@CtreateTime : 2020/04/24 10:02
@ContactEmail: joey_gosson@sina.com
'''
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class GetBrowser(object):
    """
    这是一个使用上下文管理器获取浏览器对象的类
    """

    def __init__(self, header_less=False):
        """初始化"""
        self.header_less = header_less
        self.browser = None

    def __enter__(self):
        """进入上下文管理器"""
        self.create_browser()
        if self.browser:
            return self.browser

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文管理器"""
        if self.browser:
            self.browser.quit()
            print("浏览器成功关闭")

    def create_browser(self):
        """生成浏览器对象"""
        if self.header_less:  # 无头
            options = Options()  # 创建驱动浏览器设置参数
            options.add_argument('--headless')  # 无头
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-gpu')  # 规避部署时bug
            print("完成")
            self.browser = webdriver.Chrome(chrome_options=options)
            # desired_capabilities = webdriver.DesiredCapabilities.INTERNETEXPLORER.copy() # 添加代理等参数
            # desired_capabilities['proxy'] = {
            #     "httpProxy": None,
            #     "ftpProxy": None,
            #     "sslProxy": None,
            #     "noProxy": None,
            #     "proxyType": "MANUAL",
            #     "class": "org.openqa.selenium.Proxy",
            #     "autodetect": False
            # }
            # browser = webdriver.Chrome(desired_capabilities=desired_capabilities, chrome_options=options)
        else:  # 有界面
            print("完成")
            self.browser = webdriver.Chrome()


if __name__ == "__main__":
    browser = GetBrowser()
    with browser as b:
        b.get("https://www.qiushibaike.com/article/123025050")
        raise TabError
        b.get("https://www.qiushibaike.com/text/")

    print("测试完毕")

