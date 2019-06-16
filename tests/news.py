import hashlib
import time

import requests

TOKEN = '7463bc8e-894f-11e9-9405-be63b5b3b608'
AUTH_SECRET = r'flw4\-t94!09tesldfgio30'


def calc_sign(get_data: dict, post_data: dict) -> dict:
    get = ''
    for e in sorted(get_data):
        get = get + e + '=' + str(get_data[e]) + '&'
    get = get[:-1]

    post = ''
    for e in sorted(post_data):
        post = post + e + "=" + str(post_data[e]) + "&"
    post = post[:-1]

    params = get + post + AUTH_SECRET
    return hashlib.md5(params.encode('utf-8')).hexdigest()


def news_all(begin, count):
    get_data = {
        'token': TOKEN,
        'time': int(time.time()),
        'from': begin,
        'count': count
    }
    get_data['sign'] = calc_sign(get_data, {})
    r = requests.get("http://mp.junyi.pw:8000/news/all", params=get_data)
    return r.text


def news_faculty(faculty_id, begin, count):
    get_data = {
        'token': TOKEN,
        'time': int(time.time()),
        'from': begin,
        'count': count
    }
    get_data['sign'] = calc_sign(get_data, {})
    r = requests.get("http://mp.junyi.pw:8000/news/faculty/" +
                     str(faculty_id), params=get_data)
    return r.text


def news_department(department_id, begin, count):
    get_data = {
        'token': TOKEN,
        'time': int(time.time()),
        'from': begin,
        'count': count
    }
    get_data['sign'] = calc_sign(get_data, {})
    r = requests.get("http://mp.junyi.pw:8000/news/department/" +
                     str(department_id), params=get_data)
    return r.text


# j = json.loads(news_all(1, 3))
# print(json.dumps(j))
# print(j, len(j['news']))
# print(news_department('圖書館', 1, 2))
print(news_faculty('商學院', 1, 2))
# news_faculty()
