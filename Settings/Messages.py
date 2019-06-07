# ALL API
OK = ""
WARNING = "警告（一般可忽略）"
INTERNAL_ERROR = "内部错误"
PAGE_NOT_FOUND = "页面未找到 （404）"
MISSING_FIELD = "缺少字段"

LOGIN_OTHER_ERROR = "其他错误"
LOGIN_RSA_ERROR = "登录 RSA 校验失败"
LOGIN_USERNAME_INVALID = "登录用户名无效"
LOGIN_PASSWORD_ERROR = "密码错误"
LOGIN_CAPTCHA_ERROR = "验证码错误"
LOGIN_FIELD_ERROR = "个别字段错误"

AUTH_UNKNOWN_ERROR = "未知错误"
AUTH_SIGN_VERIFICATION_FAILED = "sign 验证失败"
AUTH_TIME_INVALID = "请求已过期"
AUTH_TOKEN_INVALID = "token 无效"
AUTH_REQUEST_METHOD_ERROR = "请求方法错误"
AUTH_VALIDATE_ARGUMENT_ERROR = "校验参数错误"

# /course/comments
COURSE_UNKNOWN_ERROR = "课程 未知错误"
COURSE_COMMENT_UNKNOWN_ERROR = "评论 未知错误"
COURSE_ID_NOT_FOUNT = "未找到课程ID"
COURSE_COMMENT_CONTENT_ILLEGAL = "要评论的内容无效（非法评论内容）"
COURSE_COMMENT_CONTENT_TOO_LONG = "评论内容太长"
COURSE_COMMENT_CONTENT_EMPTY = "评论内容不能为空"
COURSE_COMMENT_ID_NOT_FOUND = "删除评论时未找到该评论ID"
COURSE_COMMENT_RANK_INVALID = "给课程的打分值不合法"
COURSE_RECORD_FROM_INVALID = "获取评论时，从第from条开始获取，from参数无效"

# GET /course/ftp
COURSE_FTP_ID_NOT_FOUNT = "课程ID未找到"

# POST /course/ftp
COURSE_FTP_ID_NOT_FOUNT = COURSE_FTP_ID_NOT_FOUNT
COURSE_FTP_HOST_ILLEGAL = "FTP 主机名非法"
COURSE_FTP_USERNAME_ILLEGAL = "FTP 用户名非法"
COURSE_FTP_PASSWORD_ILLEGAL = "FTP 密码非法"

# GET /teacher
TEACHER_ID_NOT_FOUNT = "未找到教师ID"

# POST /my/profile
PROFILE_UNKNOWN_ERROR = "未知错误"
PROFILE_NICKNAME_ILLEGAL = "昵称非法"
PROFILE_SIGNATURE_ILLEGAL = "个性签名非法"
PROFILE_AVATAR_INVALID = "头像URL不合法"
PROFILE_REFRESH_USER_NOT_FOUND = "从COES获取最新信息失败：找不到用户"
PROFILE_REFRESH_COOKIES_EXPIRED = "从COES获取最新信息失败：用户Cookie失效"

# GET /my/timetable.py
TIMETABLE_UNKNOWN_EXCEPTION = "未知异常"
TIMETABLE_SEMESTER_INVALID = "学期无效"
TIMETABLE_WEEK_INVALID = "周数无效"
TIMETABLE_COOKIE_EXPIRED = "Timetable 请求中发现 COES Cookie 过期"

# GET /user/space
SPACE_USERNAME_INVALID = "用户名无效"

OTHER_ARGUMENT_INVALID = "其它类型参数错误"
