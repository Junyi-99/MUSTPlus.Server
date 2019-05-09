from django.db import models


# 部门
class Department(models.Model):
    name_zh = models.CharField(max_length=32)
    name_en = models.CharField(max_length=64)

    def __str__(self):
        return self.name_zh


# 学院
class Faculty(models.Model):
    name_zh = models.CharField(max_length=32)
    name_en = models.CharField(max_length=64)

    def __str__(self):
        return self.name_zh


# 专业
class Major(models.Model):
    name_zh = models.CharField(max_length=32)
    name_en = models.CharField(max_length=64)
    faculty_id = models.ForeignKey(Faculty, on_delete=models.CASCADE)  # belongs to which faculty

    def __str__(self):
        return self.name_zh


# 教师
class ClassRoom(models.Model):
    name_zh = models.CharField(max_length=32)
    name_en = models.CharField(max_length=64)

    def __str__(self):
        return self.name_zh


# 文件（适用于 downContent ）
class Document(models.Model):
    department_id = models.ForeignKey(Department, on_delete=models.PROTECT, null=True)  # 来自部门
    faculty_id = models.ForeignKey(Faculty, on_delete=models.PROTECT, null=True)  # 来自学院
    title = models.CharField(max_length=128)  # 文件标题
    publish_time = models.DateField()  # 通知发布时间
    url = models.TextField()  # URL

    def __str__(self):
        return self.title


# 通告（适用于 viewContent ）
class Announcement(models.Model):
    department_id = models.ForeignKey(Department, on_delete=models.PROTECT, null=True)  # 来自部门
    faculty_id = models.ForeignKey(Faculty, on_delete=models.PROTECT, null=True)  # 来自学院
    title = models.CharField(max_length=128)  # 通知标题
    content = models.TextField()  # 通知内容
    publish_time = models.DateField()  # 通知发布时间

    def __str__(self):
        return self.title


# 附件(适用于 viewContent中的附件)
class Attachment(models.Model):
    title = models.CharField(max_length=128)  # 附件标题
    url = models.TextField()  # URL
    belongs_to = models.ForeignKey(Announcement, on_delete=models.CASCADE)  # 属于哪个 Announcement

    def __str__(self):
        return self.title


# 科目信息
class Course(models.Model):
    course_id = models.CharField(max_length=10)  # 课程ID
    course_class = models.CharField(max_length=10)  # 班别
    name_zh = models.CharField(max_length=30)
    name_en = models.CharField(max_length=30)
    name_short = models.CharField(max_length=30)
    credit = models.IntegerField(default=0)
    faculty_id = models.ForeignKey(Faculty, on_delete=models.PROTECT)
    classroom_id = models.ForeignKey(ClassRoom, on_delete=models.PROTECT)
    date_start = models.DateField()
    date_end = models.DateField()
    time_start = models.TimeField()
    time_end = models.TimeField()

    def __str__(self):
        return self.course_id + " " + self.name_zh

    class Meta:
        unique_together = (("course_id", "course_class"),)


# 学生
class Student(models.Model):
    student_id = models.CharField(max_length=18, primary_key=True)
    name_zh = models.CharField(max_length=16)
    name_en = models.CharField(max_length=16)
    faculty_id = models.ForeignKey(Faculty, on_delete=models.PROTECT)
    major_id = models.ForeignKey(Major, on_delete=models.PROTECT)
    nickname = models.CharField(max_length=64)
    sign = models.CharField(max_length=256)  # 个性签名
    sex = models.BooleanField()  # 性别 男性为True
    birthday = models.DateField()
    avatar_url = models.TextField(default="")
    experience = models.IntegerField()  # 用户经验
    token = models.CharField(max_length=64)  # 登录 token

    def __str__(self):
        return self.student_id + "(" + self.name_zh + "_"


# 老师
class Teacher(models.Model):
    name_zh = models.CharField(max_length=16)  # 中文名
    name_en = models.CharField(max_length=64)  # 英文名
    faculty_id = models.ForeignKey(Faculty, on_delete=models.PROTECT)
    avatar_url = models.TextField(default="")  # 头像
    position = models.CharField(max_length=32)  # 职位
    email = models.CharField(max_length=64)  # 电子邮件地址
    office_room = models.TextField(default="")  # 办公室
    office_hour = models.TextField(default="")  # 办公时间

    def __str__(self):
        return self.name_zh


# 老师教什么课
class TeacherTeachCourse(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


# 学生选什么课
class StudentTakeCourse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


# 科目评论
class CommentCourse(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.PROTECT)  # 被评论的课程id
    student_id = models.ForeignKey(Student, on_delete=models.PROTECT)  # 评论发布者id
    thumbs_up = models.IntegerField(default=0)  # 点赞数量
    thumbs_down = models.IntegerField(default=0)  # 点赞数量
    rank = models.IntegerField(default=3)  # 评分
    content = models.TextField  # 评论正文
    publish_time = models.TimeField()  # 发布时间
    visible = models.BooleanField()  # 是否可见


# 哪个学生认为哪条评论赞
class StudentThumbsUpCommentCourse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    comment = models.ForeignKey(CommentCourse, on_delete=models.CASCADE)


# 哪个学生认为哪条评论差
class StudentThumbsDownCommentCourse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    comment = models.ForeignKey(CommentCourse, on_delete=models.CASCADE)


# FTP
class FTP(models.Model):
    username = models.CharField(max_length=32, default='')  # ftp的用户名
    password = models.CharField(max_length=32, default='')  # ftp的密码
    course_id = models.ForeignKey(Course, on_delete=models.PROTECT)  # ftp的所属课程
    provide_by = models.ForeignKey(Student, on_delete=models.CASCADE)  # 由哪个学生提供
