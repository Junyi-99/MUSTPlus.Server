## **获取教师信息**

  该 API 用于获取一个教师的详细信息

- **URL**

  _/teacher/{teacher_name_zh}_

- **Method**

  `GET`

- **REST Params**
  `teacher_name_zh: string` 教师姓名
  
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
      "name_zh":"羅少龍",
      "name_en":"unspecified",
      "faculty":"",
      "avatar_url":"",
      "position":null,
      "email":null,
      "office_room":"",
      "office_hour":"",
      "courses":[
          {
              "intake":1909,
              "course_code":"CS108",
              "name_zh":"數據庫系統進階",
              "credit":null,
              "faculty":null
          },
          {
              "intake":1902,
              "course_code":"CS101",
              "name_zh":"數據庫系統",
              "credit":null,
              "faculty":null
          },
          {
              "intake":1709,
              "course_code":"CN103",
              "name_zh":"計算機程序設計 I",
              "credit":null,
              "faculty":null
          }
      ]
  }
  ```
  
- **Error Response:**

  ```json
  {
      "code": -1000, 
      "msg": "未知错误"
  }
  ```

  ```json
  {
      "code": -5000,
      "msg": "未找到教师"
  }
  ```

  就这俩返回，加上AUTH里面的全部

- **Example** (Python)

  写文档累死了不写例子了要看例子请移步UnitTest！！！！！！
  ~~（累死我了啊啊啊啊啊啊）~~