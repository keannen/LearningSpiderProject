from selenium import webdriver

driver = webdriver.Chrome()
driver.get(url='https://maoyan.com/board/4')

def patse_html():
    # 1.节点对象列表
    dd_list = driver.find_elements_by_xpath('//*[@id="app"]/div/div/div[1]/dl/dd')
    for dd in dd_list:
        # text属性：获取当前节点以及子节点后后代节点文本内容
        one_film_list = dd.text.split('\n')
        item = {}
        item['number'] = one_film_list[0].strip()
        item['name'] = one_film_list[1].strip()
        item['star'] = one_film_list[2].strip()
        item['time'] = one_film_list[3].strip()
        item['score'] = one_film_list[4].strip()
        print(item)
        # print(dd.text)
        # print('*'*50)

while True:
    patse_html()
    try:
        # selenium在找不到节点时会抛出异常
        driver.find_element_by_partial_link_text('下一页').click()
    except:
        driver.quit()
        break