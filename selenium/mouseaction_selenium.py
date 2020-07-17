"""
打开百度首页,移动到设置节点,点击高级搜索
"""
from selenium import webdriver
# 导入鼠标事件
from selenium.webdriver import ActionChains
import time

driver = webdriver.Chrome()
driver.maximize_window()
#  get():等着页面元素加载完后才会继续执行代码
driver.get(url='http://www.baidu.com/')
# 1.鼠标移动到设置节点
set_node = driver.find_element_by_xpath('//*[@id="s-usersetting-top"]')
# 操作鼠标三步走
ActionChains(driver).move_to_element(to_element=set_node).perform()

# 高级搜索节点并点击
# 一定！一定！一定要给页面预留加载时间
time.sleep(2)
driver.find_element_by_link_text('高级搜索').click()

