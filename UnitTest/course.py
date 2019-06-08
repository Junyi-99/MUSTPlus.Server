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


def course(course_id):
    get_data = {
        'token': TOKEN,
        'time': int(time.time()),
    }

    get_data['sign'] = calc_sign(get_data, {})
    r = requests.get("http://mp.junyi.pw:8000/course/" +
                     str(course_id), params=get_data)
    print(r.text)


def comment_get(course_id):
    get_data = {
        'token': TOKEN,
        'time': int(time.time()),
    }

    get_data['sign'] = calc_sign(get_data, {})
    r = requests.get("http://mp.junyi.pw:8000/course/" +
                     str(course_id) + "/comment", params=get_data)
    print(r.text)


def comment_post(course_id, rank, content):
    get_data = {
        'token': TOKEN,
        'time': int(time.time()),
    }
    post_data = {
        'rank': rank,
        'content': content
    }

    get_data['sign'] = calc_sign(get_data, post_data)
    r = requests.post("http://mp.junyi.pw:8000/course/" +
                      str(course_id) + "/comment", params=get_data, data=post_data)
    print(r.text)


def comment_delete(course_id, comment_id):
    get_data = {
        'token': TOKEN,
        'time': int(time.time()),
        'id': comment_id,
    }

    get_data['sign'] = calc_sign(get_data, {})
    r = requests.delete("http://mp.junyi.pw:8000/course/" +
                        str(course_id) + "/comment", params=get_data)
    print(r.text)

# comment_post(5, 8, "   ")
# comment_delete(5, 1)
# comment_get(5)
# course(5)
# comment_get(5)
