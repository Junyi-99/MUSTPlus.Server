# 这个文件主要是与COES连接的部分，现在包括COES的登录
# 个人信息和课程表的获取
import requests

from settings import urls

LOGIN_SUCCESSFUL = 0
LOGIN_PASSWORD_ERROR = 1
LOGIN_CAPTCHA_ERROR = 2
LOGIN_STUDENT_ID_DOES_NOT_EXIST = 3

LOGIN_OTHER_ERROR = 10


# 获取 token 和 cookie
def get_token_cookies():
    headers = urls.headers
    headers['Accept-Language'] = 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7'

    ret = requests.get(url="https://coes-stud.must.edu.mo/coes/login.do", headers=headers)
    pos1 = ret.text.find('org.apache.struts.taglib.html.TOKEN') + 44  # 44 代表 这里面一大串和外面的value=" 的长度
    pos2 = ret.text.find('">', pos1)

    cookies = ""
    for cookie in ret.cookies:
        cookies = cookies + cookie.name + "=" + cookie.value + "; "
    return ret.text[pos1:pos2], cookies[:-2]  # remove the last '; '


def get_captcha(cookies):
    headers = urls.headers
    headers['Cookie'] = cookies
    ret = requests.get(url='https://coes-stud.must.edu.mo/coes/RandomImgCode.do', headers=headers)
    return ret.content


# 登录COES 成功返回0，密码错误返回1，验证码错误返回2，其他错误返回3
def login(username, password, token, cookies, captcha='0000'):
    try:
        url = 'https://coes-stud.must.edu.mo/coes/login.do'
        data = {
            'org.apache.struts.taglib.html.TOKEN': token,
            'userid': username,
            'password': password,
            'randCode': captcha,
            'submit': '登入',
        }
        headers = urls.headers
        headers['Cookie'] = cookies
        ret = requests.post(url=url, data=data, headers=headers)
        # print(r.text)
        # with open("login_record.html", 'wb') as file:
        #     file.write(ret.text.encode('utf-8'))
        #     file.close()

        trait = '- Inbox'
        if trait in ret.text:
            # pos1 = ret.text.find(trait) + len(trait)
            # pos2 = ret.text.find('-->', pos1)
            # print("Login Successful!")
            # print("coes Version: ", ret.text[pos1:pos2])

            return LOGIN_SUCCESSFUL
        if '驗證碼不相同' in ret.text:
            logout(cookies)
            return LOGIN_CAPTCHA_ERROR
        if '找不到.' in ret.text:
            return LOGIN_STUDENT_ID_DOES_NOT_EXIST
        if '密碼錯誤' in ret.text:
            return LOGIN_PASSWORD_ERROR

        pos1 = ret.text.rfind('alert')
        pos2 = ret.text.find(');', pos1)
        return ret.text[pos1 + 7:pos2 - 1]
    except Exception as exception:
        print(exception)
        logout(cookies)


def logout(cookies):
    print("Trying to logout", cookies)
    # headers = URLS.headers
    # headers['Cookie'] = cookies
    # requests.post(url=URLS.COES_LOGOUT, headers=headers)
