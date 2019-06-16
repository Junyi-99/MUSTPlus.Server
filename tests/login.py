import base64
import json
import getpass
import requests
import rsa
import sys


print("Trying to get basic information ... ")
r = requests.get('http://mp.junyi.pw:8000/auth/hash')
j = json.loads(r.text)
key = j['key']
token = j['token']
cookies = j['cookies']
captcha = j['captcha']
pic = base64.b64decode(captcha.encode('utf-8'))

# save captcha
with open("./capt.jpg", 'wb') as f:
    f.write(pic)
    f.close()

# prompt input
captcha = input("Please input the Captcha: ")
if len(sys.argv) > 1:
    with open(sys.argv[1], 'r') as f:
        username = f.readline().strip()
        password = f.readline().strip()
        print(username, password)
else:
    username = input("Please input your student id: ")
    password = getpass.getpass("And your password: ")

data = {
    'username': username.encode('utf-8'),
    'password': password.encode('utf-8'),
    'token': token.encode('utf-8'),
    'cookies': cookies.encode('utf-8'),
    'captcha': captcha.encode('utf-8'),
}

# 加密部分
# print("RSA Enctyption ... ")
pk = rsa.PublicKey.load_pkcs1(key.encode('utf-8'))
for k in data:
    data[k] = base64.b64encode(rsa.encrypt(data[k], pk))
# print("Done ... !")


print("Trying login ...")
r = requests.post('http://mp.junyi.pw:8000/auth/login', data=data)
print("Server Response:")
print(json.loads(r.text))
