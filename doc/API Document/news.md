## **获取全部资讯**

  获取 intranet 上的全部通告

- **URL**

  _/news/all_

- **Method**

  `GET`
  
- **REST Params**
  
  None
  
- **URL Params**

  **Required**

  `token: string` 登陆时获得的 token

  `time: integer` 10位时间戳 UTC+0

  `sign: string` 当前请求的签名

  **Optional**

  `from: integer` 从哪一条开始获取（范围∈ [1, n]）

  `count: integer` 获取多少条（范围∈ [1, 20]）

  （虽然不用担心传错可选数据，因为服务端会进行二次参数过滤，确保稳定）

  （但是客户端还是要保证数据正常，不能光靠后端的稳定来支撑）

  （客户端使用这两个可选参数可以实现信息流功能，即一次显示X条，下拉显示更多）

- **Data Params**

  None

- **Success Response:**

  ```JSON
  {
      "code":0,
      "msg":"",
      "records":869, # 总数据条数
      "news":[
          {
              "fac_dep":"總務處",
              "title":"學校商戶於暑假的營業時間",
              "date":"2019-06-05",
              "type":false,
              "url":"downContent('12289');"
          },
          {
              "fac_dep":"酒店與旅遊管理學院",
              "title":"2019年畢業典禮事宜",
              "date":"2019-06-04",
              "type":false,
              "url":"downContent('12287');"
          },
          {
              "fac_dep":"教務處",
              "title":"2019本科課程暑期重要行事曆",
              "date":"2019-05-31",
              "type":false,
              "url":"downContent('12286');"
          }
      ]
  }
  ```

- **Error Response:**

  ```json
  {
      "code": -4200, 
      "msg": "资讯 未知错误"
  }
  ```

  | Value              | Message       | Code  |
  | ------------------ | ------------- | ----- |
  | NEWS_UNKNOWN_ERROR | 资讯 未知错误 | -4200 |
  

GET 请求里，只会返回**这一个**错误代码 + AUTH系列的错误代码



## **获取某一部门的资讯**

  获取某一个部门的资讯，与获取全部资讯的处理方法一致


- **URL**

  _/news/department/{department_name_zh}_

- **Method**

  `GET`
  
- **REST Params**
  
  `department_name_zh: string` 部门名（所有部门名可以从‘获取部门列表’接口获取）
  
- **URL Params**

  **Required**

  `token: string` 登陆时获得的 token

  `time: integer` 10位时间戳 UTC+0

  `sign: string` 当前请求的签名

  **Optional**

  `from: integer` 从哪一条开始获取（范围∈ [1, n]）

  `count: integer` 获取多少条（范围∈ [1, 20]）

  （同上）

- **Data Params**

  None

- **Success Response:**

  ```JSON
  {
      "code":0,
      "msg":"",
      "records":2,
      "news":[
          {
              "fac_dep":"圖書館",
              "title":"圖書館於暑假期間開館時間通告",
              "date":"2019-05-30",
              "type":false,
              "url":"downContent('12285');"
          },
          {
              "fac_dep":"圖書館",
              "title":"1909學期訂書、繳費及領書通知",
              "date":"2019-05-06",
              "type":true,
              "content":"<TD></TD><TD></TD>",
              "attachments":[
                  {
                      "title":"1909學期訂書、繳費及領書通知",
                      "url":"downContent('12201');"
                  },
                  {
                      "title":"1909學期訂書、繳費及領書須知",
                      "url":"downContent('12202');"
                  }
              ]
          }
      ]
  }
  ```

- **Error Response:**

  ```json
  {
      "code": -4200, 
      "msg": "资讯 未知错误"
  }
  ```

  | Value              | Message       | Code  |
  | ------------------ | ------------- | ----- |
  | NEWS_UNKNOWN_ERROR | 资讯 未知错误 | -4200 |
  

GET 请求里，只会返回**这一个**错误代码 + AUTH系列的错误代码

## **获取某一学院的资讯**

  获取某一个部门的资讯，与获取全部资讯的处理方法一致


- **URL**

  _/news/faculty/{faculty_name_zh}_

- **Method**

  `GET`
  
- **REST Params**
  
  `faculty_name_zh: string` 学院名（所有学院名可以从‘获取学院列表’接口获取）
  
- **URL Params**

  **Required**

  `token: string` 登陆时获得的 token

  `time: integer` 10位时间戳 UTC+0

  `sign: string` 当前请求的签名

  **Optional**

  `from: integer` 从哪一条开始获取（范围∈ [1, n]）

  `count: integer` 获取多少条（范围∈ [1, 20]）

  （同上）

- **Data Params**

  None

- **Success Response:**

  ```JSON
  {
    "code":0,
    "msg":"",
    "records":136,
    "news":[
        {
            "fac_dep":"商學院",
            "title":"通知：更改期末考試地點(O401及O402)",
            "date":"2019-05-30",
            "type":false,
            "url":"downContent('12281');"
        },
        {
            "fac_dep":"商學院",
            "title":"補課：BBAZ16202 財務報表分析(E1)",
            "date":"2019-05-14",
            "type":false,
            "url":"downContent('12253');"
        }
    ]
}
  ```

- **Error Response:**

  ```json
  {
      "code": -4200, 
      "msg": "资讯 未知错误"
  }
  ```

  | Value              | Message       | Code  |
  | ------------------ | ------------- | ----- |
  | NEWS_UNKNOWN_ERROR | 资讯 未知错误 | -4200 |
  

GET 请求里，只会返回**这一个**错误代码 + AUTH系列的错误代码

  

## **获取Banners**（该接口还未实现）

  获取资讯页面上方的banners


- **URL**

  _/news/bannners_

- **Method**

  `GET`
  
- **REST Params**
  
  None
  
- **URL Params**

  **Required**

  `token: string` 登陆时获得的 token

  `time: integer` 10位时间戳 UTC+0

  `sign: string` 当前请求的签名

- **Data Params**

  None

- **Success Response:**

  ```JSON
  该接口还未实现
  ```
  
- **Error Response:**

  ```json
  该接口还未实现
  ```
  
  | Value          | Message        | Code           |
  | -------------- | -------------- | -------------- |
| 该接口还未实现 | 该接口还未实现 | 该接口还未实现 |
  



  

