## **获取课程详情**

  该 API 用于获取一个课程的详细内容。通过直接指定 URL 中的 `{course_id}` 即可获得某课程的详细信息

- **URL**

  _/course/{course_id}_

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
      "course_code":"GWC001",
      "course_class":"D03",
      "name_zh":"西方文化通論",
      "name_en":null,
      "name_short":null,
      "credit":null,
      "faculty":null,
      "teachers":[
          {
              "name_zh":"顧衛民",
              "name_en":"unspecified",
              "position":null,
              "email":null,
              "office_room":"",
              "avatar":""
          },
          {
              "name_zh":"許平",
              "name_en":"unspecified",
              "position":null,
              "email":null,
              "office_room":"",
              "avatar":""
          },
          {
              "name_zh":"趙林",
              "name_en":"unspecified",
              "position":null,
              "email":null,
              "office_room":"",
              "avatar":""
          }
      ],
      "schedule":[
          {
              "intake":1709,
              "date_begin":"09-04",
              "date_end":"12-16",
              "time_begin":"15:00",
              "time_end":"16:45",
              "day_of_week":1,
              "classroom":"N214"
          }
      ],
      "rank":3.5 # 可能为 null
  }
  ```

- **Error Response:**

  ```json
  {
      "code": -4002, 
      "msg": "未找到该课程ID"
  }
  ```

  

- **Example** (Python)

  ```python
  import hashlib
  import json
  import time
  import requests
  
  TOKEN = '7463bc8e-894f-11e9-9405-be63b5b3b608'
  AUTH_SECRET = r'flw4\-t94!09tesldfgio30'
  
  
  def calc_sign(get_data: dict, post_data: dict) -> dict:
      get = ''
      for e in sorted(get_data):
          get = get + e + '=' + str(get_data[e]) + '&'
      get = get[:-1]
  
      post = ''
      for e in sorted(post_data):
          post = post+e+"="+str(post_data[e]) + "&"
      post = post[:-1]
  
      params = get + post + AUTH_SECRET
      print(params)
      return hashlib.md5(params.encode('utf-8')).hexdigest()
  
  def course(course_id):
      get_data = {
          'token': TOKEN,
          'time': int(time.time()),
      }
  
      get_data['sign'] = calc_sign(get_data, {})
      r = requests.get("http://mp.junyi.pw:8000/course/" +
                       str(course_id), params=get_data)
      print(r.text)
  
  course(5)
  ```
  
  

