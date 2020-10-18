## **登录（DEPRECATED）**

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
      "msg": "其他错误"
  }
  ```
  
  ```JSON
  {
      "code": -901,
      "msg": "RSA签名无效"
  }
  ```
  
  
  状态码范围 [`-905` , `-900`]，返回不带 `detail` 参数
  
  状态码详情请查阅 状态码文档