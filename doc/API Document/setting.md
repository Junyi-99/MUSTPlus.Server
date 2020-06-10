## **获取用户设置**

  用来获取当前学生的自定义设置，显示在 setting 页面上

- **URL**

  _/setting_

- **Method**

  `GET`

- **REST Params**
  
  None

- **URL Params**

  **Required:**

  `token: string` 登陆时获得的 token

  `time: integer` 10位时间戳 UTC+0

  `sign: string` 当前请求的签名

- **Data Params**

  None

- **调用成功返回样例**

  ```JSON
    {
        "code":0,
        "msg":"",
        "settings":{
            "nt_score":true,
            "nt_academic":true,
            "nt_cet":true,
            "nt_dormitory":true,
            "nt_course":true,
            "nt_course_registration":true,
            "nt_book_return":true,
            "nt_book_borrow":true,
            "nt_study_room":true,
            "nt_catastrophe":true
        }
    }
  ```
  
  以上返回数据仅供参考，请以实际返回数据为准
  
  说明：
  
  `nt_` 前缀代表 Notification
  
  `nt_score`: 是否开启成绩提醒
  
  `nt_academic`: 是否开启学院消息提醒
  
  `nt_cet`: 是否开启四六级提醒
  
  `nt_dormitory`: 是否开启宿舍相关信息提醒
  
  `nt_course`: 是否开启上课提醒
  
  `nt_course_registration`: 是否开启选课提醒
  
  `nt_book_return`: 是否开启还书提醒
  
  `nt_book_borrow`: 是否开启借书提醒（书到了可以借了）
  
  `nt_study_room`: 是否开启自习室可用提醒
  
  `nt_catastrophe`: 是否开启自然灾害提醒

- **Error Response:**

  会遇到 AUTH 系列的错误（用户未登录或未经授权的访问）


## **更新用户设置**

  用来更新某个设置项。注意，为了后端写起来简单，更新用户设置只能单条单条的更新，不能一次更新一堆设置。

- **URL**

  _/setting_

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

  **Required:**
  
  `setting: string` 要设置的字段（比如 GET /setting 之后服务器返回的settings里有个叫 nt_cet 的字段，那这里就能够填 nt_cet）
  
  `value: int` 如果是 true 就写 1， 如果是 false 就写 0

- **调用成功返回样例**

  ```JSON
    {
        "code":0,
        "msg":""
    }
  ```

  
  目前 setting 参数可以接受的有：
  
  `nt_score`: 是否开启成绩提醒
  
  `nt_academic`: 是否开启学院消息提醒
  
  `nt_cet`: 是否开启四六级提醒
  
  `nt_dormitory`: 是否开启宿舍相关信息提醒
  
  `nt_course`: 是否开启上课提醒
  
  `nt_course_registration`: 是否开启选课提醒
  
  `nt_book_return`: 是否开启还书提醒
  
  `nt_book_borrow`: 是否开启借书提醒（书到了可以借了）
  
  `nt_study_room`: 是否开启自习室可用提醒
  
  `nt_catastrophe`: 是否开启自然灾害提醒

- **Error Response:**

  会遇到 AUTH 系列的错误（用户未登录或未经授权的访问）:
  
  `AUTH_UNKNOWN_ERROR = -1000  # 未知错误`

    `AUTH_SIGN_VERIFICATION_FAILED = -1001  # sign 验证失败`
    
    `AUTH_TIME_INVALID = -1002  # 请求已过期`
    
    `AUTH_TOKEN_INVALID = -1003  # token 无效`
    
    `AUTH_REQUEST_METHOD_ERROR = -1004  # 请求方法错误`
    
    `AUTH_VALIDATE_ARGUMENT_ERROR = -1005  # 校验参数错误`
  
  还会遇到
  
  `SETTING_NO_SUCH_SETTING = -6600 # 没有这个设置`
  
  `SETTING_VALUE_TYPE_ERROR= -6601 # 值类型错误`