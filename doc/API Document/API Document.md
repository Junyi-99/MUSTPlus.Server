# MUSTPlus API 文档

所有涉及到的 API 都有对应的 Python 实现 ( 在根目录下的 UnitTest 文件夹内 )

所有的实现我都自己跑过，都没问题，如果遇到了问题还是请联系我

实现的不优雅，因为只是用来做测试

（再次强调，写文档真累死个人......）



## Authentication （登录与授权）

 [获取哈希值](auth_hash.md)
 
 [登录MUSTPlus](auth_login.md)
 
 [退出MUSTPlus](auth_logout.md)

## Basic (基本常量获取)

[获取当前学期](basic_semester.md)

[获取当前周数](basic_week.md)

## Timetable （课程表）

 [获取课程表](timetable.md)

## Course （课程信息）

[获取课程信息](course.md)

[获取课程评论信息](course_comment.md)

[发布课程评论信息](course_comment.md)

[删除课程评论信息](course_comment.md)

[给课程评论点赞](course_comment_thumbs_up.md)

[取消给课程评论点赞](course_comment_thumbs_up.md)

[给课程评论点踩](course_comment_thumbs_down.md)

[取消给课程评论点踩](course_comment_thumbs_down.md)

[获取课程FTP信息](course_ftp.md)

[发布课程FTP信息](course_ftp.md)

[删除课程FTP信息](course_ftp.md)

## News （资讯）

[获取全部资讯](news.md)

[获取某一学院的资讯](news.md)

[获取某一部门的资讯](news.md)

[获取Banners](news.md)

## Student （学生信息）

[获取学生信息](student.md)

[获取学生的设置选项](student_settings.md)

[更新学生的设置选项](student_settings.md)



## Teacher （教师信息）

[获取教师信息](teacher.md)

[给教师点赞](teacher_like.md)

## Moment （校友圈）

**可发布匿名动态到校友圈！**



名词说明：

**动态**：用户在校友圈中发布的内容称为动态（类似于QQ空间的说说）

**匿名动态**：为了增加娱乐性，用户可以隐藏身份在校友圈中发布动态。

注意：该功能并不能真正隐藏用户，匿名动态仍然接受内容审查，并可追踪到不良、非法内容的发布者。


[获取广告](moment_ad.md)

后续将广告植入到获取 {校友圈内容} API 中

### [匿名动态](moment_anonymous.md)

- [查询可用匿名次数](moment_anonymoud.md)

### [动态](moment.md)

- [发布](moment.md)

  动态发布默认为全校可见。

- [转载](moment.md)

- [删除](moment.md)

- [修改](moment.md)

- [获取](moment.md)

  - [校友圈动态](moment.md)
  
  - [我发布的动态](moment.md)

  用户应可以设置浏览时要屏蔽的人或学院。每条动态显示评论条数和点赞条数，不显示具体内容
  
- [赞](moment_like.md)

- [取消赞](moment_like.md)

### [多媒体](moment_media.md)

- [上传图片](moment_picture.md)

  (为了节约储存资源，所有上传到服务器的媒体都要经过压缩)

- [上传视频](moment_video.md)

  (上传视频待定)

### [屏蔽](moment_block.md)

- [屏蔽某人](moment_block.md)

- [屏蔽某学院](moment_block.md)

### [评论](moment_comment.md)

- [评论一条校友圈](moment_comment.md)

- [删除对动态的评论](moment_comment.md)

- [获取一条动态的评论](moment_comment.md)

## Extendable Apps (可扩展服务)

### [反馈](feedback.md)

### [成绩查询](grade.md)

### [公交查询](bus.md)

- [珠海公交](bus_zhuhai.md)

- [澳门公交](bus_macau.md)

### [食堂](restaurant.md)

- [今日常餐](restaurant_daily.md)

### [图书馆](library.md)

- [图书查询](library_search.md)

- [借书查询](library_borrow.md)

- [图书续借](library_)

  应该在界面上写明[操作指引](http://lib.must.edu.mo/node/164)
  
- [借书预约](library_booking.md)

- [房间预约](library_booking.md)

### [填表](forms.md)

- [在线填表](forms.md)
  
  此功能需跟学校产生合作
  
  或接入图书馆预约打印系统