## **给课程评论点赞👍**

  赞某一个课程的评论。注意，这个API的comment_id 放在 URL 参数里，因为要美观

- **URL**

  _/course/thumbs_up_

- **Method**

  `POST`

- **REST Params**

  None

- **URL Params**

  **Required**

  `token: string` 登陆时获得的 token

  `time: integer` 10位时间戳 UTC+0

  `sign: string` 当前请求的签名

  `id: integer` 课程评论ID

- **Data Params**

  None

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



## **取消给课程评论点赞❌👍**

  取消赞某一个课程的评论。与点赞不同的，只有REQUEST METHOD的区别

- **URL**

  _/course/thumbs_up_

- **Method**

  `DELETE`

- **REST Params**
  
  None

- **URL Params**

  **Required**

  `token: string` 登陆时获得的 token

  `time: integer` 10位时间戳 UTC+0

  `sign: string` 当前请求的签名

  `id: integer` 课程评论ID

- **Data Params**

  None

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

