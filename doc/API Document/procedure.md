# 整体流程

## 程序启动
 1. GET    [获取学期](basic_semester.md)
 2. GET    [获取当前周是当前学期的第几周](basic_week.md)

## 登录部分

 1. GET    [登录前获取哈希值](auth_hash.md)
 2. POST   [登录](auth_login.md)
 3. GET    [获取个人信息]
 4. POST   [登出](auth_logout.md)
 4. 课表部分
 5. 校友圈部分
 6. 通告部分
 7. 个人设置部分
  
 ## 课表部分
 
 1. GET    [获取课程表](timetable.md)
 2. GET    [查看课程详细信息]
 3. GET    [获取当前课程的评价]
 3. POST   [发布当前课程的评价]
 4. DELETE [删除当前课程的评价]
 4. GET    [查看老师详细信息]
 
## 校友圈部分
 
 1. GET    [获取校友圈列表](moment.md)
 2. GET    [获取单条校友圈详情](moment_id.md)
 3. UPDATE [修改校友圈内容](moment_id.md)
 4. DELETE [删除校友圈](moment_id.md)
 5. POST   [发布校友圈](moment.md)
 6. POST   [给校友圈点赞]
 7. POST   [评论某条校友圈]
 8. POST   [评论某条校友圈下的评论]

## 通告部分

1. GET     [获取通告]
2. GET     [获取某学院通告]
3. GET     [获取文件类型通告]
4. GET     [获取通知类型通告]

