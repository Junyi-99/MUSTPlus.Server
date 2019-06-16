## **获取课程表📅**

  该 API 用于获取当前学生的课表

- **URL**

  _/timetable_

- **Method**

  `GET`

- **REST Params**
  None
  
- **URL Params**

  **Required**

  `token: string` 登陆时获得的 token

  `time: integer` 10位时间戳 UTC+0

  `sign: string` 当前请求的签名

  `week: integer` 第几周（第0周表示总表，周数可以通过"获取周数"接口获取）

  **Optional**

  `intake: integer` 学期，不指定的话默认以服务器上的学期为主

- **Data Params**

  None

- **Success Response:**

  ```JSON
  {
      "code":0,
      "msg":"",
      "timetable":[
          {
              "day":"02",
              "time_begin":"15:00",
              "time_end":"16:45",
              "course_code":"CS101",
              "course_name_zh":"數據庫系統",
              "course_class":"D2",
              "classroom":"C308",
              "teacher":"羅少龍",
              "date_begin":"1-14",
              "date_end":"5-18",
              "course_id":20
          },
          {
              "day":"05",
              "time_begin":"11:00",
              "time_end":"12:45",
              "course_code":"CS101",
              "course_name_zh":"數據庫系統",
              "course_class":"D2",
              "classroom":"C308",
              "teacher":"羅少龍",
              "date_begin":"1-14",
              "date_end":"5-18",
              "course_id":20
          },
          {
              "day":"01",
              "time_begin":"15:00",
              "time_end":"16:45",
              "course_code":"CE107",
              "course_name_zh":"數字電路基礎",
              "course_class":"D1",
              "classroom":"C309",
              "teacher":"李平",
              "date_begin":"1-14",
              "date_end":"5-18",
              "course_id":21
          },
          {
              "day":"04",
              "time_begin":"15:00",
              "time_end":"16:45",
              "course_code":"CE107",
              "course_name_zh":"數字電路基礎",
              "course_class":"D1",
              "classroom":"O609(納米黑板)",
              "teacher":"李平",
              "date_begin":"1-14",
              "date_end":"5-18",
              "course_id":21
          },
          {
              "day":"03",
              "time_begin":"10:00",
              "time_end":"12:40",
              "course_code":"CN105",
              "course_name_zh":"Web技術概論",
              "course_class":"D1",
              "classroom":"C408（實驗室）",
              "teacher":"趙慶林",
              "date_begin":"1-14",
              "date_end":"5-18",
              "course_id":22
          },
          {
              "day":"02",
              "time_begin":"10:00",
              "time_end":"12:40",
              "course_code":"LP104",
              "course_name_zh":"面向對象程序設計",
              "course_class":"D1",
              "classroom":"O609(納米黑板)",
              "teacher":"梁寶",
              "date_begin":"1-14",
              "date_end":"5-18",
              "course_id":23
          },
          {
              "day":"03",
              "time_begin":"15:00",
              "time_end":"17:40",
              "course_code":"LP104",
              "course_name_zh":"面向對象程序設計",
              "course_class":"D1",
              "classroom":"C408（實驗室）",
              "teacher":"梁寶",
              "date_begin":"1-14",
              "date_end":"5-18",
              "course_id":23
          }
      ]
  }
  ```
  
- **Error Response:**

  ```json
  {
      "code": -7003, 
      "msg": timetable
  }
  ```

  | Value                       | Message                               | Code  |
  | --------------------------- | ------------------------------------- | ----- |
  | TIMETABLE_UNKNOWN_EXCEPTION | 未知异常                              | -7000 |
  | TIMETABLE_SEMESTER_INVALID  | 学期无效                              | -7001 |
  | TIMETABLE_WEEK_INVALID      | 周数无效                              | -7002 |
  | TIMETABLE_COOKIE_EXPIRED    | Timetable 请求中发现 COES Cookie 过期 | -7003 |

GET 请求里，只会返回**这些**错误代码 + AUTH系列的错误代码

- **Example** (Python)

  不想写Example了，写文档快累死了
  
  