from selenium import webdriver
import time

# 创建浏览器
browser = webdriver.firefox()
browser.get('http://www.baidu.com')

#窗口最大化
browser.maximize_window()


# 5 秒后关闭浏览器
time.sleep(5)
browser.quit()