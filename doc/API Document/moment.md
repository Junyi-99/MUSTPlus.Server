## **获取校友圈列表 📃**

  该 API 用于获取一个校友圈列表，一般是打开校友圈时首先调用该API。通过直接指定 URL 中的 `{moment_id}` 即可获得某课程的详细信息。
  
  校友圈部分：
  
   1. **获取校友圈列表 (打开QQ空间/微信朋友圈)** <-- 你所在的步骤
   2. 获取单条校友圈详情 (点击查看详情，比如评论、图片等)
   3. 修改校友圈内容 (如果有权限)
   4. 删除校友圈
   5. 给校友圈点赞
  

- **URL**

  _/moment

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
  
  `from: integer` (10位时间戳 UTC+0) 获取发布时间在 from 时间之前的校友圈 
      

- **Data Params**

  None

- **Success Response:**

  ```JSON
 
  ```

- **Error Response:**

  ```JSON

  ```

  

- **Example** (Python)

  ```python
  
  ```
  
  

