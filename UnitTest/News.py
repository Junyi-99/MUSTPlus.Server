import json
from random import randint

import requests

#
# all = "http://mp.junyi.pw:8000/news/banners/"
# banners = "http://mp.junyi.pw:8000/news/all/"

for i in range(0, 2000):
    department_id = "http://mp.junyi.pw:8000/news/department/" + str(randint(-9999999, 9999999))
    r = requests.get(url=department_id)
    json.loads(r.text)
    if i % 100 == 0:
        print("department Progress: %d/100" % (i / 2000 * 100))

for i in range(0, 2000):
    faculty_id = "http://mp.junyi.pw:8000/news/faculty/" + str(randint(-9999999, 9999999))
    r = requests.get(url=faculty_id)
    json.loads(r.text)
    if i % 100 == 0:
        print("faculty Progress: %d/100" % (i / 2000 * 100))
