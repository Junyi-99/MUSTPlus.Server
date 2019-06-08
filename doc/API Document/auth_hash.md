**获取哈希值**
----
  该 API 用于获取登录前的一系列所需值。

  流程：

  `获取哈希值` -> `登录` -> `获取个人信息` -> `获取课程表`

* **URL**

  _/auth/hash_

* **Method**
  
  `GET`
  
* **REST Params**

  None

*  **URL Params**

  None
  
* **Data Params**

  None

* **Success Response:**
  
  ```JSON
  {
  	"code": 0,     # 状态码
  	"msg": "",     # 错误信息
  	"key": "",     # public_key：用于后续登录时的加密
  	"token": "",   # COES Apache Token：后续登录时所需参数
  	"cookies": "", # COES captcha cookies：与验证码对应的cookie
  	"captcha": ""  # COES captcha：验证码
  }
  ```


* **Error Response:**
  No Error Conditions.

* **Example** (Python)

  ```python
  import base64
  import json
  import requests
  
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
  
  ```

  

