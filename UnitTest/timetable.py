import time
import json
import hashlib
import requests

token = 'a51127f8-85e0-11e9-9405-be63b5b3b608'

data = {
    'token': token,
    'time': int(time.time())
}

params = ''
for e in sorted(data):
    params = params + e + '=' + str(data[e]) + '&'
params = params[:-1]

data['sign'] = hashlib.md5(params.encode('utf-8')).hexdigest()
# print(data)
r = requests.get("http://mp.junyi.pw:8000/timetable", params=data)

print(json.loads(r.text))
