from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def jd_spider(url,keyword):
    driver = webdriver.Chrome()
    driver.get(url)
    input_tag = driver.find_element_by_id('key')
    input_tag.send_keys(keyword)
    input_tag.send_keys(Keys.ENTER)
    time.sleep(5)
    get_goods(driver)

def get_goods(driver):
    goods = driver.find_elements_by_class_name('gl-item')
    for good in goods:
        link = good.find_element_by_tag_name('a').get_attribute('href')
        name = good.find_element_by_css_selector('.p-name em').text.replace('\n','')
        price = good.find_element_by_css_selector('.p-price i').text
        commit = good.find_element_by_css_selector('.p-commit a').text
        shop = good.find_element_by_css_selector('.p-shop a').text

        msg = '''
            商品:%s
            链接:%s
            价格:%s
            评论:%s
            商店:%s
        '''%(name,link,price,commit,shop)
        print(msg)

        #获取大量数据
        button = driver.find_element_by_partial_link_text('下一页')
        button.click()
        time.sleep(1)
        get_goods(driver)

jd_spider('https://www.jd.com/','口罩')