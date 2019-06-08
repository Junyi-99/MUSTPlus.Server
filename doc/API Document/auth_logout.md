## **登出**

  该 API 用于登出 MUSTPlus。参数只有标准的3个用于校验的

- **URL**

  _/auth/logout_

- **Method**

  `POST`

- **REST Params**
  
  None
  

- **URL Params**

  **Required:**

  `token: string` 登陆时获得的 token

  `time: integer` 10位时间戳 UTC+0

  `sign: string` 当前请求的签名

- **Data Params**

  None

- **Success Response:**

  ```JSON
  {
  	"code": 0,  # 状态码
  	"msg": "",  # 错误信息
  }
  ```

- **Error Response:**

  None

* **Example** (Python)

  无~~（太简单了这个 Example 就不写了）~~

