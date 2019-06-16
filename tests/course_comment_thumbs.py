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


def thumbs_up(course_id, comment_id, up: bool):
    get_data = {
        'token': TOKEN,
        'time': int(time.time()),
        'id': comment_id
    }
    get_data['sign'] = calc_sign(get_data, {})

    url = "http://mp.junyi.pw:8000/course/%d/comment/thumbs_up" % course_id
    if up:
        r = requests.post(url, params=get_data)
    else:
        r = requests.delete(url, params=get_data)
    print(r.text)


def thumbs_down(course_id, comment_id, up: bool):
    get_data = {
        'token': TOKEN,
        'time': int(time.time()),
        'id': comment_id
    }
    get_data['sign'] = calc_sign(get_data, {})

    url = "http://mp.junyi.pw:8000/course/%d/comment/thumbs_down" % course_id
    if up:
        r = requests.post(url, params=get_data)
    else:
        r = requests.delete(url, params=get_data)
    print(r.text)


thumbs_up(5, 1, True)
thumbs_down(5, 1, True)
