import hashlib
import json
import time

import requests

token = '831d9e5c-87b0-11e9-9405-be63b5b3b608'
def t(intake, week):
    data = {
        'token': token,
        'time': int(time.time()),
        'intake': intake,
        'week':week,
    }

    params = ''
    for e in sorted(data):
        params = params + e + '=' + str(data[e]) + '&'
    params = params[:-1]

    data['sign'] = hashlib.md5(params.encode('utf-8')).hexdigest()
    # print(data)
    r = requests.get("http://mp.junyi.pw:8000/timetable", params=data)
    #print(r.text)
    print()
    print(json.loads(r.text))

t(1709,0)
t(1802, 0)
t(1809, 0)
t(1902, 0)
t(1909, 0)
