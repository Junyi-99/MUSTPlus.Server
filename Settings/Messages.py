# ALL API
OK_MSG = 'OK'  # 正常
WARNING_MSG = '警告信息'  # 警告（一般可忽略）
INTERNAL_ERROR_MSG = 'Caused an unexpected exception, your request has been recorded.' # 内部错误
PAGE_NOT_FOUND = '404'

LOGIN_RSA_ERROR_MSG = 'Login failed(Security check failed) You may have been attacked by a man-in-the-middle'
LOGIN_USERNAME_INVALID_MSG = 'Username Invalid'
LOGIN_PASSWORD_ERROR_MSG = 'Wrong Password'

AUTH_SIGN_VERIFICATION_FAILED_MSG = 'sign 验证失败'
AUTH_TIME_INVALID_MSG = '请求已过期'
AUTH_TOKEN_INVALID_MSG = 'token 无效'
AUTH_REQUEST_METHOD_ERROR_MSG = '请求方法错误'

# DELETE /course/comments
COURSE_COMMENT_ID_NOT_FOUND_MSG = '未找到课程评论ID'

# POST /course/comments
COURSE_ID_NOT_FOUNT_MSG = '未找到课程ID'
COURSE_COMMENT_CONTENT_ILLEGAL_MSG = '要评论的内容无效（非法评论内容）'
COURSE_COMMENT_CONTENT_TOO_LONG_MSG = '评论内容太长'
COURSE_COMMENT_CONTENT_EMPTY_MSG = '评论内容不能为空'

# GET /course/comments
COURSE_ID_NOT_FOUNT_MSG = COURSE_ID_NOT_FOUNT_MSG
COURSE_RECORD_FROM_INVALID_MSG = '从第from条开始获取，from参数无效'

# GET /course/ftp
COURSE_FTP_ID_NOT_FOUNT_MSG = '课程ID未找到'

# POST /course/ftp
COURSE_FTP_ID_NOT_FOUNT_MSG = COURSE_FTP_ID_NOT_FOUNT_MSG
COURSE_FTP_HOST_ILLEGAL_MSG = 'FTP 主机名非法'
COURSE_FTP_USERNAME_ILLEGAL_MSG = 'FTP 用户名非法'
COURSE_FTP_PASSWORD_ILLEGAL_MSG = 'FTP 密码非法'

# GET /course/info
COURSE_ID_NOT_FOUNT_MSG = COURSE_ID_NOT_FOUNT_MSG  # 未找到课程ID

# GET /teacher
TEACHER_ID_NOT_FOUNT_MSG = '未找到教师ID'

# POST /my/profile
PROFILE_NICKNAME_ILLEGAL_MSG = '昵称非法'
PROFILE_SIGNATURE_ILLEGAL_MSG = '个性签名非法'
PROFILE_AVATAR_INVALID_MSG = '头像URL不合法'

# GET /my/timetable
TIMETABLE_SEMESTER_INVALID_MSG = '学期无效'
TIMETABLE_WEEK_INVALID_MSG = '周数无效'

# GET /user/space
SPACE_USERNAME_INVALID_MSG = '用户名无效'


OTHER_ARGUMENT_INVALID_MSG = '其它类型参数错误'
