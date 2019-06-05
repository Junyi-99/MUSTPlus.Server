# 这个文件主要是与COES连接的部分，现在包括COES的登录
# 个人信息和课程表的获取
import requests

from Settings import URLS

LOGIN_SUCCESSFUL = 0
LOGIN_PASSWORD_ERROR = 1
LOGIN_CAPTCHA_ERROR = 2
LOGIN_STUDENT_ID_DOES_NOT_EXIST = 3

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
        # print(r.text)
        with open("login_record.html", 'wb') as f:
            f.write(r.text.encode('utf-8'))
            f.close()
        trait = '<!--COES VERSION '
        if trait in r.text:
            p1 = r.text.find(trait) + len(trait)
            p2 = r.text.find('-->', p1)
            version = r.text[p1:p2]
            print("Login Successful!")
            print("COES Version: ", version)
            return LOGIN_SUCCESSFUL
        elif '驗證碼不相同' in r.text:
            logout(cookies)
            return LOGIN_CAPTCHA_ERROR
        elif '找不到.' in r.text:
            return LOGIN_STUDENT_ID_DOES_NOT_EXIST
        elif '密碼錯誤' in r.text:
            return LOGIN_PASSWORD_ERROR
        else:
            find2 = r.text.rfind('alert')
            find3 = r.text.find(');', find2)
            return r.text[find2 + 7:find3 - 1]
    except Exception as e:
        print(e)
        logout(cookies)


def logout(cookies):
    print("Trying to logout")
    # headers = URLS.headers
    # headers['Cookie'] = cookies
    # requests.post(url=URLS.COES_LOGOUT, headers=headers)
