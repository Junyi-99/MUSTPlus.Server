## **给课程评论点踩👎**

  踩某一个课程的评论

- **URL**

  _/course/{course_id}/comment/thumbs_down_

- **Method**

  `POST`

- **REST Params**
  `course_id: integer`

- **URL Params**

  **Required**

  `token: string` 登陆时获得的 token

  `time: integer` 10位时间戳 UTC+0

  `sign: string` 当前请求的签名

  `id: integer` 课程评论ID

- **Data Params**

  None (注意，就算这里是POST方法，id参数也要放在URLParams里)

- **Success Response:**

  ```JSON
  {
      "code":0,
      "msg":""
  }
  ```

- **Error Response:**

  ```json
  {
      "code": -4006, 
      "msg": "未找到该评论ID"
  }
  ```

  | Value                       | Message        | Code  |
  | --------------------------- | -------------- | ----- |
  | COURSE_COMMENT_ID_NOT_FOUND | 未找到该评论ID | -4006 |
  | AUTH_REQUEST_METHOD_ERROR   | 请求方法错误   | -1004 |

  POST 请求里，只会返回**这些**错误代码 + AUTH系列的错误代码



## **取消给课程评论点踩❌👎**

  取消踩某一课程的评论

- **URL**

  _/course/{course_id}/comment/thumbs_down_

- **Method**

  `DELETE`

- **REST Params**
  `course_id: integer` 

- **URL Params**

  **Required**

  `token: string` 登陆时获得的 token

  `time: integer` 10位时间戳 UTC+0

  `sign: string` 当前请求的签名

  `id: integer` 课程评论ID

- **Data Params**

  None (注意，就算这里是POST方法，id参数也要放在URLParams里)

- **Success Response:**

  ```JSON
  {
      "code":0,
      "msg":""
  }
  ```

- **Error Response:**

  ```json
  {
      "code": -4006, # 状态码 
      "msg": "未找到该评论ID" # 错误信息
  }
  ```

  | Value                       | Message        | Code  |
  | --------------------------- | -------------- | ----- |
  | COURSE_COMMENT_ID_NOT_FOUND | 未找到该评论ID | -4006 |
  | AUTH_REQUEST_METHOD_ERROR   | 请求方法错误   | -1004 |

  DELETE 请求里，只会返回**这些**错误代码 + AUTH系列的错误代码

