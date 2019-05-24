# 这个文件主要是与COES连接的部分，现在包括COES的登录
# 个人信息和课程表的获取
import time
from lxml import etree
import requests
from django.core.exceptions import ObjectDoesNotExist

from Settings import Codes
from Settings import URLS

LOGIN_SUCCESSFUL = 0
LOGIN_PASSWORD_ERROR = 1
LOGIN_CAPTCHA_ERROR = 2
LOGIN_OTHER_ERROR = 10


# 获取 token 和 cookie
def get_token_cookies():
    headers = URLS.headers
    headers['Accept-Language'] = 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7'

    r = requests.get(url="https://coes-stud.must.edu.mo/coes/login.do", headers=headers)
    p1 = r.text.find('org.apache.struts.taglib.html.TOKEN') + 44  # 44 代表 这里面一大串和外面的value=" 的长度
    p2 = r.text.find('">', p1)

    cookies = ""
    for c in r.cookies:
        cookies = cookies + c.name + "=" + c.value + "; "
    return r.text[p1:p2], cookies[:-2]  # remove the last '; '


def captcha(cookies):
    headers = URLS.headers
    headers['Cookie'] = cookies
    r = requests.get(url='https://coes-stud.must.edu.mo/coes/RandomImgCode.do', headers=headers)
    return r.content


def student_information(cookies):
    headers = URLS.headers
    headers['Cookie'] = cookies
    headers['Accept-Language'] = 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7'
    result = {}  # 结果字典

    title = ('student_id', 'name_zh', 'name_en', 'gender',
             'birthday', 'birthplace', 'nationality')
    r = requests.get(url='https://coes-stud.must.edu.mo/coes/StudentInfo.do', headers=headers)

    html = etree.HTML(r.text)
    info = html.xpath("//td[@class='data']/table[1]")  # 注意这里是table[1]而不是table[1]/tbody，学校coes没有按照标准html写（妈的）
    print(info)
    for i in range(1, 8):
        result[title[i - 1]] = info[0].xpath("./tr[%d]/td[2]/text()" % (i,))[0].strip()

    print("StudentInfo OK")

    title = ('faculty', 'program', 'major', 'description',
             'remarks', 'require_credit', 'effective_intake')
    r = requests.get(url='https://coes-stud.must.edu.mo/coes/StudyPlanGroup.do', headers=headers)
    html = etree.HTML(r.text)
    info = html.xpath("//td[@class='data']/table[1]")  # 注意这里是table[1]而不是table[1]/tbody，学校coes没有按照标准html写（妈的）
    for i in range(1, 8):
        result[title[i - 1]] = info[0].xpath("./tr[%d]/td[2]/text()" % (i,))[0].strip()

    return result


# 登录COES 成功返回0，密码错误返回1，验证码错误返回2，其他错误返回3
def login(username, password, token, cookies, captcha='0000'):
    try:
        data = {
            'org.apache.struts.taglib.html.TOKEN': token,
            'userid': username,
            'password': password,
            'randCode': captcha,
            'submit': '登入',
        }
        headers = URLS.headers
        headers['Cookie'] = cookies
        r = requests.post(url='https://coes-stud.must.edu.mo/coes/login.do', data=data, headers=headers)

        trait = '<!--COES VERSION '
        if trait in r.text:
            p1 = r.text.find(trait) + len(trait)
            p2 = r.text.find('-->', p1)
            version = r.text[p1:p2]
            print("Login Successful!")
            print("COES Version: ", version)
            return LOGIN_SUCCESSFUL
        elif 'Please ' in r.text:
            print(r.text)
            logout(cookies)
            return LOGIN_CAPTCHA_ERROR
    except Exception as e:
        print(e)
        logout(cookies)


def logout(cookies):
    print("Trying to logout")
    # headers = URLS.headers
    # headers['Cookie'] = cookies
    # requests.post(url=URLS.COES_LOGOUT, headers=headers)
