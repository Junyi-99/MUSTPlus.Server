import time

import requests
from django.core.exceptions import ObjectDoesNotExist

from MUSTPlus.models import Student


def get_token(body):
    token_simple = '49057506de26d2ea640cea1847d7f3d5'
    target = 'org.apache.struts.taglib.html.TOKEN" value="'
    pos = body.find(target) + target.__len__()
    return body[pos:pos + token_simple.__len__()]


def verify(userid, password):
    url = 'https://coes-stud.must.edu.mo/coes/login.do'
    r = requests.get(url=url)
    token = get_token(r.text)
    data = {
        'userid': userid,
        'password': password,
        'submit': 'Login',
        'org.apache.struts.taglib.html.TOKEN': token
    }
    time.sleep(3.0)
    r = requests.post(url=url, data=data)
    url = 'https://coes-stud.must.edu.mo/coes/logout.do'
    requests.post(url=url, cookies=r.cookies)
    if r.text.find('<!--COES VERSION ') == -1:
        return False
    else:
        return True


def get_cookie(userid, password):
    if verify(userid, password):
        url = 'https://coes-stud.must.edu.mo/coes/login.do'
        r = requests.get(url=url)
        token = get_token(r.text)
        data = {
            'userid': userid,
            'password': password,
            'submit': 'Login',
            'org.apache.struts.taglib.html.TOKEN': token
        }
        time.sleep(3.0)
        r = requests.post(url=url, data=data)
        return r.cookies
    else:
        return 0


def get_info(userid, password):
    try:
        student = Student.objects.get(student_id=userid)
    except ObjectDoesNotExist:
        student = Student.objects.create(student_id=userid)
    cookies = get_cookie(userid, password)
    if cookies == 0:
        return 0
    url = 'https://coes-stud.must.edu.mo/coes/StudentInfo.do'
    r = requests.post(url=url, cookies=cookies)
