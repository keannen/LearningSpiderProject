"""
模拟登录qq邮箱
"""
from selenium import webdriver

driver = webdriver.Chrome()
driver.get(url='https://mail.qq.com/')

# 切换到iframe子页面
# node = driver.find_element_by_id('login_frame')
# driver.switch_to.frame(node)
# 找到用户名节点 密码 登录按钮
driver.find_element_by_xpath('//*[@id="u"]').send_keys('QQ账号')
driver.find_element_by_xpath('//*[@id="p"]').send_keys('QQ密码')
driver.find_element_by_xpath('//*[@id="login_button"]').click()











