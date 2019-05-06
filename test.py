# Author : Aikov
# Time :2019/4/30
# Status: Finished
# 登录 COES ，登录成功返回 cookie，失败返回 None
import os
import time

import requests

# Author : Aikov
# Time :2019/4/30
# Status:Finished
# 获取 Apache Token
from Settings import URLS


def get_token(body):
    token_simple = '49057506de26d2ea640cea1847d7f3d5'
    target = 'org.apache.struts.taglib.html.TOKEN" value="'
    pos = body.find(target) + target.__len__()
    return body[pos:pos + token_simple.__len__()]


def login(username, password, lang):
    r = requests.get(url=URLS.LOGIN_URL)
    token = get_token(r.text)
    data = {
        'userid': username,
        'password': password,
        'submit': 'Login' if lang == 'en' else '登入',
        'org.apache.struts.taglib.html.TOKEN': token
    }
    print(data)
    time.sleep(5.0)

    r = requests.post(url=URLS.LOGIN_URL, data=data)
    print(r.text)
    if r.text.find('<!--COES VERSION ') == -1:
        return None
    else:
        return r.cookies


# 退出 COES
def logout(cookies):
    requests.post(url=URLS.LOGOUT_URL, cookies=cookies)


def lo(username, password, lang='zh'):
    cookies = login(username, password, lang)
    if cookies is None:
        print("Login failed")
        return None

    try:
        r1 = requests.get(url=URLS.STUDENT_INFO_URL, cookies=cookies, headers=URLS.headers).text
        r2 = requests.get(url=URLS.STUDY_PLAN_GROUP_URL, cookies=cookies, headers=URLS.headers).text
        with open(os.path.dirname(os.path.abspath( __file__))+"/r1.html", "wb") as f:
            f.write(r1)
            f.close()
        with open(os.path.dirname(os.path.abspath( __file__))+"/r2.html", "wb") as f:
            f.write(r2)
            f.close()
    finally:
        logout(cookies)


lo("1709853D-I011-0021", "34205608")
print("ok")
