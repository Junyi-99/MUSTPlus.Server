## **登录**

  该 API 用于登录 MUSTPlus，为保证安全，采用 POST 请求，并且请求参数全部使用 RSA 加密

- **URL**

  _/auth/login_

- **Method**

  `POST`
  
- **REST Params**
  
  None
  
- **URL Params**

  None

- **Data Params**

   _在这个 API 中，所有的参数都要经过 `base64(rsa_encrypt(content, pk))` 处理（伪代码）_

   _content 为要加密内容_

   _pk 为公钥_

   **Required:**

   `username: string`

   `password: string`

   `token: string`

   `cookies: string`

   `captcha: string`

   **Optional:**

   None

- **Success Response:**

  ```JSON
  {
  	"code": 0,     	         # 状态码
  	"msg": "",     	         # 错误信息
  	"student_name": "张三",   # 学生姓名
  	"token": "1d98580a-8810-11e9-9405-be63b5b3b608",
      # MUSTPlus Token：后续API请求时用来表明身份
  }
  ```
  
- **Error Response:**

  ```JSON
  {
      "code": -900,
      "msg": "其他错误",
      "detail": "详细错误原因"
  }
  ```
  
  ```JSON
  {
      "code": -901,
      "msg": "RSA签名无效"
  }
  ```
  
  状态码范围 [`-900`, `-900`]，返回带 `detail` 参数
  
  状态码范围 [`-901` , `-905`]，返回不带 `detail` 参数
  
  状态码详情请查阅 状态码文档
  
- **Example** (Python)

   ```python
   # 接 auth_hash.md 中的 Example
   import base64
   import json
   import getpass
   import requests
   import rsa
   
   # get public_key and something we need
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
   username = input("Please input your student id: ")
   password = getpass.getpass("And your password: ")
   
   post_data = {
       'username': username.encode('utf-8'),
       'password': password.encode('utf-8'),
       'token': token.encode('utf-8'),
       'cookies': cookies.encode('utf-8'),
       'captcha': captcha.encode('utf-8'),
   }
   
   # RSA 加密部分
   pk = rsa.PublicKey.load_pkcs1(key.encode('utf-8'))
   for k in data:
       data[k] = base64.b64encode(rsa.encrypt(data[k], pk))
   
   # 请求登录
   r = requests.post('http://mp.junyi.pw:8000/auth/login', data=post_data)
   print(json.loads(r.text))
   
   ```
```
   
   


```