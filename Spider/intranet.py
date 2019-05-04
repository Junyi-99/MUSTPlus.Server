import requests
from MUSTPlus import coes_url


def login():
    data = {
        'lang': 'BIG5',
        'studno': '1709853di011002',
        'passwd': '34205608',
        'submit': '提交'
    }
    # 职业素养
    headers = {
        'User-Agent': 'MUSTPlus/5.0 (Server Spider 1.0; Ubuntu; x64)',
    }
    r = requests.post(url=coes_url.INTRANET_LOGIN_URL, data=data, headers=headers)
    print(r.text)