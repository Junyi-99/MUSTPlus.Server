from django.db import models


# 部门
class Department(models.Model):
    name = models.CharField(max_length=30)


# 学院
class Faculty(models.Model):
    name = models.CharField(max_length=30)


# 专业
class Major(models.Model):
    name = models.CharField(max_length=30)
    faculty_id = models.ForeignKey(Faculty, on_delete=models.CASCADE)


# 教师
class ClassRoom(models.Model):
    name = models.CharField(max_length=30)


# 通告
class Announcement(models.Model):
    department_id = models.ForeignKey(Department, on_delete=models.PROTECT)  # 来自部门
    faculty_id = models.ForeignKey(Faculty, on_delete=models.PROTECT)  # 来自学院
    title = models.CharField(max_length=128)  # 通知标题
    content = models.TextField()  # 通知内容
    publish_time = models.TimeField()  # 通知发布时间


# 附件
class Attachment(models.Model):
    title = models.CharField(max_length=128)  # 附件标题
    url = models.TextField()  # URL
    belongs_to = models.ForeignKey(Announcement, on_delete=models.CASCADE)  # 属于哪个 Announcement


# 科目信息
class Course(models.Model):
    course_id = models.CharField(max_length=10, primary_key=True)  # 课程ID
    course_class = models.CharField(max_length=10, primary_key=True)  # 班别
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


# 学生
class Student(models.Model):
    student_id = models.CharField(max_length=18, primary_key=True)
    name_zh = models.CharField(max_length=16)
    name_en = models.CharField(max_length=16)
    faculty_id = models.ForeignKey(Faculty, on_delete=models.PROTECT)
    major_id = models.ForeignKey(Major, on_delete=models.PROTECT)
    nickname = models.CharField(max_length=64)
    sign = models.CharField(max_length=256)  # 个性签名
    sex = models.BooleanField()
    birthday = models.DateField()
    avatar_url = models.TextField(default="")
    experience = models.IntegerField(max_length=20)  # 用户经验
    token = models.CharField(max_length=64)  # 登录 token


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

#科目评论
class CourseComments(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.SET_NULL, to_field=Student.student_id)
    course_id = models.ForeignKey(Course, on_delete=models.SET_NULL, to_field=Course.course_id)
    course_class = models.ForeignKey(Course, on_delete=models.SET_NULL, to_field=Course.course_class)
    thumbs_up = models.IntegerField(default=0)
    rank = models.IntegerField(default=5)
    content = models.TextField(default="")
    publish_time = models.TimeField()
    visible = models.BooleanField()
