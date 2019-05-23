import requests
import base64
import json
import rsa

print("Trying to get basic information ... ")

r = requests.get('http://mp.junyi.pw:8000/auth/hash')
j = json.loads(r.text)
key = j['key']
token = j['token']
cookies = j['cookies']
captcha = j['captcha']
pic = base64.b64decode(captcha.encode('utf-8'))

with open("capt.jpg", 'wb') as f:
    f.write(pic)
    f.close()

captcha = input("Please input the Captcha: ")

data = {
    'username': 'YOUR_USERNAME'.encode('utf-8'),
    'password': 'YOUR_PASSWORD'.encode('utf-8'),
    'token': token.encode('utf-8'),
    'cookies': cookies.encode('utf-8'),
    'captcha': captcha.encode('utf-8'),
}

# 加密部分
print("RSA Enctyption ... ")
pk = rsa.PublicKey.load_pkcs1(key.encode('utf-8'))
for k in data:
    data[k] = base64.b64encode(rsa.encrypt(data[k], pk))
print("Done ... !")

print()
print("Trying login to MUST+ ...")
r = requests.post('http://mp.junyi.pw:8000/auth/login', data=data)
print()
print("Server Response:")
print(r.text)

