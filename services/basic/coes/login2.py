# 这个文件主要是与COES连接的部分，现在包括COES的登录
# 个人信息和课程表的获取

import sys
import traceback

import requests
# 移除安全警告
import urllib3

from settings import urls

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LOGIN_SUCCESSFUL = 0
LOGIN_INVALID_CREDENTIALS = 1
LOGIN_OTHER_ERROR = 10


# 登录COES 成功返回0，密码错误返回1，其他错误返回10
# 返回 cookie 内容
def login(username, password):
    try:
        url = 'https://login.must.edu.mo/login'
        data = {
            'username': username,
            'password': password,
            'execution': 'e1s1',
            '_eventId': 'submit',
            'geolocation': ''
        }
        headers = urls.headers

        # 新的 i.must.edu.mo 首先要获取 cookie 里的 SESSION， 然后拿着 SESSION 去 login
        ret = requests.get(url=url)
        ret = requests.post(url=url, data=data, cookies=ret.cookies, headers=headers, proxies={}, verify=False,
                            timeout=5)

        trait = 'admin/profile.do'
        if trait in ret.text:
            cookies = ''
            for cookie in ret.cookies:
                cookies = cookie.name+"=" + cookie.value
            return LOGIN_SUCCESSFUL, cookies
        if 'Invalid credentials.' in ret.text:
            return LOGIN_INVALID_CREDENTIALS, ''
        else:
            return LOGIN_OTHER_ERROR, ''

    except Exception as exception:
        # 新版登入系统不需要退出原有账号即可再次登入
        print(exception)
        traceback.print_exc(file=sys.stdout)
        return LOGIN_OTHER_ERROR, ''


def logout(cookies):
    pass
