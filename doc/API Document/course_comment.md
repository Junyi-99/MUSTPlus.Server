## **获取课程评论👀**

  该 API 用于获取一个课程的详细内容。通过直接指定 URL 中的 `{course_id}` 即可获得某课程的详细信息

- **URL**

  _/course/{course_id}/comment_

- **Method**

  `GET`

- **REST Params**
  `course_id: integer` 是 course_id 不是 course_code ！这里要注意！

- **URL Params**

  **Required**

  `token: string` 登陆时获得的 token

  `time: integer` 10位时间戳 UTC+0

  `sign: string` 当前请求的签名

- **Data Params**

  None

- **Success Response:**

  ```JSON
  {
      "code":0,
      "msg":"",
      "comment":[
          {
              "comment_id":2,
              "student_id":"1709853D-I011-0021",
              "thumbs_up":0,
              "thumbs_down":0,
              "rank":5,
              "content":"感觉课程不错呀！",
              "publish_time":"2019-06-07 18:14:47"
          },
          {
              "comment_id":1,
              "student_id":"1709853D-I011-0021",
              "thumbs_up":0,
              "thumbs_down":0,
              "rank":1,
              "content":"差死了",
              "publish_time":"2019-06-07 18:14:33"
          }
      ]
  }
  ```

- **Error Response:**

  ```json
  {
      "code": -4001, 
      "msg": "评论 未知错误"
  }
  ```

  ```json
  {
      "code": -4002, 
      "msg": "未找到课程ID"
  }
  ```

  GET 请求里，只会返回这**两个**错误代码 + AUTH系列的错误代码



## **发布课程评论**✍

  该 API 用于获取一个课程的详细内容。通过直接指定 URL 中的 `{course_id}` 即可获得某课程的详细信息

- **URL**

  _/course/{course_id}/comment_

- **Method**

  `POST`

- **REST Params**
  `course_id: integer` 是 course_id 不是 course_code ！这里要注意！

- **URL Params**

  **Required**

  `token: string` 登陆时获得的 token

  `time: integer` 10位时间戳 UTC+0

  `sign: string` 当前请求的签名

- **Data Params**

  **Required**

  `rank: integer` 给课程的评分

  `content: string` 评论内容

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
      "code": -4001, # 状态码 
      "msg": "评论 未知错误" # 错误信息
  }
  ```

  | Value                           | Message              | Code  |
  | ------------------------------- | -------------------- | ----- |
  | COURSE_COMMENT_UNKNOWN_ERROR    | 课程评论 未知错误    | -4001 |
  | COURSE_ID_NOT_FOUNT             | 未找到课程ID         | -4002 |
  | COURSE_COMMENT_CONTENT_TOO_LONG | 评论内容太长         | -4004 |
  | COURSE_COMMENT_CONTENT_EMPTY    | 评论内容为空         | -4005 |
| COURSE_COMMENT_RANK_INVALID     | 给课程的打分值不合法 | -4007 |
  
  POST请求里，只会返回**这些**错误代码 + AUTH系列的错误代码

## **删除课程评论❌**

  该 API 用于删除某条课程评论。删除课程评论后，对于课程的评分也会被删除。

- **URL**

  _/course/{course_id}/comment_

- **Method**

  `DELETE`

- **REST Params**
  `course_id: integer` 是 course_id 不是 course_code ！这里要注意！

- **URL Params**

  **Required**

  `token: string` 登陆时获得的 token

  `time: integer` 10位时间戳 UTC+0

  `sign: string` 当前请求的签名
  
  `id: integer` 课程评论 ID

- **Data Params**

- 
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
      "code": -4006, # 状态码 
      "msg": "未找到该评论ID" # 错误信息
  }
  ```

  DELETE 请求里，只会返回这**一个**错误代码 + AUTH系列的错误代码
  
- **附录：**

  有可能在实现API的时候会产生这样一个疑问：

  _明明 course_id 与 coursecomment_id 没有附属关系，我直接给 coursecomment_id 不就好了，为什么还要传入 course_id 呢？_

  好问题。

  主要是为了 API **风格上的统一**，所以采用了现在这种实现方式。