import time
import requests
import random
from hashlib import md5

class youdaoSpider(object):
    # 初始化变量
    def __init__(self):
        # url一定为F12抓到的 headers -> General -> Request URL
        self.url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
        self.headers = {
            # 检查频率最高的3个
            "Cookie":  "_ntes_nnid=c000407b48c3c6564b628015fd31facd,1594090394299; OUTFOX_SEARCH_USER_ID_NCOO=1039079104.217199; OUTFOX_SEARCH_USER_ID=-121227433@10.169.0.102; JSESSIONID=aaaGjJJkaWXiHbFVvWfnx; ___rl__test__cookies=1594608199941",
            "Referer":  "http://fanyi.youdao.com/",
            "User-Agent":  "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
            }

    # 伪造salt、sign、ts
    def get_salt_sign_ts(self,word):
        # ts
        ts = str(int(time.time()*1000))
        # salt
        salt = ts + str(random.randint(0,9))
        # sign md5的随机值每段时间都会改变,每次爬取前需要更新【mmbP%A-r6U3Nw(n]BjuEU】
        # string = "fanyideskweb" + word + salt + "n%A-rKaT5fb[Gy?;N5@Tj"
        string =  "fanyideskweb" + word + salt + "mmbP%A-r6U3Nw(n]BjuEU"
        s = md5()
        s.update(string.encode())
        sign = s.hexdigest()
        return salt,sign,ts

    # 请求主函数
    def attack_yd(self,word):
        # 1. 先拿到salt,sign,ts
        salt,sign,ts = self.get_salt_sign_ts(word)
        # 2. 定义form表单数据为字典: data={}
        # 检查了salt sign
        data = {
            "i": word,
            "from": "AUTO",
            "to": "AUTO",
            "smartresult": "dict",
            "client": "fanyideskweb",
            "salt": salt,
            "sign": sign,
            "ts": ts,
            "bv": "7e3150ecbdf9de52dc355751b074cf60",
            "doctype": "json",
            "version": "2.1",
            "keyfrom": "fanyi.web",
            "action": "FY_BY_REALTlME",
        }
        # 3. 直接发请求:requests.post(url,data=data,headers=xxx)
        html = requests.post(
            url = self.url,
            data = data,
            headers = self.headers
        ).json()
        # res.json() 将json格式的字符串转为python数据类型

        test_result = html['translateResult']
        result = html['translateResult'][0][0]['tgt']
        print(result)
        print(test_result)

    # 启动函数
    def run(self):
        # 输入单词
        word = input('请输入翻译的单词')
        self.attack_yd(word)

if __name__ == '__main__':
    spider = youdaoSpider()
    spider.run()