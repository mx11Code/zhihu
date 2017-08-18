import requests
import os
import json

import time

from bs4 import BeautifulSoup


def login():
    url = 'http://www.zhihu.com'
    loginURL = 'http://www.zhihu.com/login/phone_num'
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
        "Connection": "keep-alive",
        "Content-Length": "138",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        # "Cookie": 'q_c1=8e652a76f4d34610b8a9dddf7236105c|1499929596000|1499929596000; _zap=3ea6a12a-afce-4ef3-b795-42c6f65542dd; d_c0="ADBCDBQLDwyPTk_AQkSsGJ6tRrKp0y-iCkc=|1499947967"; q_c1=8e652a76f4d34610b8a9dddf7236105c|1502635335000|1499929596000; aliyungf_tc=AQAAAISwvnTprAIATwlvcRfAcjzgJDwU; _xsrf=c20a9159-6b7b-4ff1-9e63-bd3b389d07f8; r_cap_id="MjA0YTFjMjQxZGM3NDQ1MDgwNjdkY2NkNjA2OTBlNWI=|1502895934|09ad58520c3c7d691351721bb2fe86fb0913f58f"; cap_id="Yzc4OTE2NWFmNTljNDY1N2FkMWZlZjY2MWRjNTE0NGM=|1502895934|47f65e85fadbf3cf8c0da890f6451ddf5dd1e32d"; l_cap_id="ODczOTNlNDY5MWE4NDE3MDhkMDBjZGNhN2M2OTU2MWU=|1502896212|d83e1d3aa8c1b1cf1bd8df304c8a98076526bfe0"; __utma=51854390.919594198.1499947969.1502809446.1502893926.28; __utmb=51854390.0.10.1502893926; __utmc=51854390; __utmz=51854390.1502893926.28.23.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=51854390.000--|2=registration_date=20170816=1^3=entry_date=20170713=1',
        "Host": "www.zhihu.com",
        "Origin": "https://www.zhihu.com",
        "Referer": "https://www.zhihu.com/?next=%2Fsettings%2Faccount",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "X-Xsrftoken": "c20a9159-6b7b-4ff1-9e63-bd3b389d07f8",
    }
    data = {
        'phone_num': '13128201060',
        'password': '123456098765',
        "captcha_type": "cn"
    }
    global s
    s = requests.session()
    global xsrf
    if os.path.exists('cookiefile'):
        with open('cookiefile') as f:
            cookie = json.load(f)
        s.cookies.update(cookie)
        req1 = s.get(url, headers=headers)
        soup = BeautifulSoup(req1.text, "html.parser")
        xsrf = soup.find('input', {'name': '_xsrf', 'type': 'hidden'}).get('value')
        # 建立一个zhihu.html文件,用于验证是否登陆成功
        with open('zhihu.html', 'w') as f:
            f.write(req1.content)
    else:
        req = s.get(url, headers=headers)
        print(req)
        soup = BeautifulSoup(req.text, "html.parser")
        xsrf = soup.find('input', {'name': '_xsrf', 'type': 'hidden'}).get('value')
        data['_xsrf'] = xsrf
        timestamp = int(time.time() * 1000)
        captchaURL = 'http://www.zhihu.com/captcha.gif?=' + str(timestamp)
        # print(captchaURL)
        with open('zhihucaptcha.gif', 'wb') as f:
            captchaREQ = s.get(captchaURL, headers=headers)
            f.write(captchaREQ.content)
        # loginCaptcha = input('input captcha:\n').strip()
        # data['captcha'] = loginCaptcha
        print(data)
        loginREQ = s.post(loginURL, headers=headers, data=data)
        print("------------>", loginREQ.text)
        # with open('response.html', 'wb') as rsp:
        #     rsp.write(loginREQ.text)
        return
        if not loginREQ.json()['r']:
            print(s.cookies.get_dict())
            with open('cookiefile', 'wb') as f:
                json.dump(s.cookies.get_dict(), f)
        else:
            print('login fail')


login()
