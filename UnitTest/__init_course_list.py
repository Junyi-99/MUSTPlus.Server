import hashlib
import json
import time

import requests

token = '1d98580a-8810-11e9-9405-be63b5b3b608'

params = ''
data = {
    'token': token,
    'time': int(time.time()),
}
params = ''
for e in sorted(data):
    params = params + e + '=' + str(data[e]) + '&'
params = params[:-1]
data['sign'] = hashlib.md5(params.encode('utf-8')).hexdigest()
r = requests.get("http://mp.junyi.pw:8000/course/init", params=data)
# print(r.text)
print()
print(json.loads(r.text))
