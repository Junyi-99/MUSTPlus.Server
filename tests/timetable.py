import hashlib
import time

import requests

TOKEN = '34773dc2-9065-11e9-9405-be63b5b3b608'
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
    print(params)
    return hashlib.md5(params.encode('utf-8')).hexdigest()
    
def t(intake, week):
    data = {
        'token': TOKEN,
        'time': int(time.time()),
        'intake': intake,
        'week':week,
    }
    data['sign'] = calc_sign(data, {})
    # print(data)
    r = requests.get("http://mp.junyi.pw:8000/timetable", params=data)
    #print(r.text)
    print(r.text)
    # print(json.loads(r.text))


# t(1709, 0)
# t(1802, 0)
t(1809, 0)
t(1902, 0)
t(1909, 0)
