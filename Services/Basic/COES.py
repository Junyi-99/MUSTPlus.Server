# 这个文件主要是与COES连接的部分，现在包括COES的登录
# 个人信息和课程表的获取
import time

import requests
from django.core.exceptions import ObjectDoesNotExist

from Settings import Codes
from Settings import URLS


def get_token_cookies():
    r = requests.get(url="https://coes-stud.must.edu.mo/coes/login.do")
    p1 = r.text.find('org.apache.struts.taglib.html.TOKEN') + 44  # 44 代表 这里面一大串和外面的value=" 的长度
    p2 = r.text.find('">', p1)
    return r.text[p1:p2], r.cookies


def captcha(token, cookies):
    j = ""
    for a in cookies:
        if a.name is "JSESSIONID":
            j = a.value

    r = requests.get(url='https://coes-stud.must.edu.mo/coes/RandomImgCode.do', cookies=cookies)


def login(username, password, token, cookies, captcha='0000', lang='zh'):
    try:
        data = {
            'org.apache.struts.taglib.html.TOKEN': token,
            'userid': username,
            'password': password,
            'randCode': captcha,
            'submit': '登入',
        }
        print(data)
        r = requests.post(
            url='https://coes-stud.must.edu.mo/coes/login.do', data=data, cookies=cookies, verify=False)
        print(r.text)

        trait = '<!--COES VERSION '
        if trait in r.text:
            p1 = r.text.find(trait) + len(trait)
            p2 = r.text.find('-->', p1)
            version = r.text[p1:p2]
            print("Login Successful!")
            print("COES Version: ", version)
    except Exception as e:
        logout(cookies)
    finally:
        logout(cookies)


def logout(cookies):
    requests.post(url=URLS.COES_LOGOUT, cookies=cookies, headers=URLS.headers)
