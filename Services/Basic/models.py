from django.db import models


# 部门
class Department(models.Model):
    name_zh = models.CharField(max_length=32, primary_key=True)
    name_en = models.CharField(max_length=64)

    def __str__(self):
        return self.name_zh


# 学院
class Faculty(models.Model):
    name_zh = models.CharField(max_length=32, primary_key=True)
    name_en = models.CharField(max_length=64)

    def __str__(self):
        return self.name_zh


# 课程
class Program(models.Model):
    name_zh = models.CharField(max_length=128, primary_key=True)
    name_en = models.CharField(max_length=128)

    def __str__(self):
        return self.name_zh


# 专业
class Major(models.Model):
    name_zh = models.CharField(max_length=32, primary_key=True)
    name_en = models.CharField(max_length=64)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)  # belongs to which faculty

    def __str__(self):
        return self.name_zh


# 教师
class ClassRoom(models.Model):
    name_zh = models.CharField(max_length=32, primary_key=True)
    name_en = models.CharField(max_length=64)

    def __str__(self):
        return self.name_zh


# 学生
class Student(models.Model):
    student_id = models.CharField(max_length=18, primary_key=True)
    name_zh = models.CharField(max_length=16, null=True)
    name_en = models.CharField(max_length=16, null=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.PROTECT, null=True)
    program = models.ForeignKey(Program, on_delete=models.PROTECT, null=True)
    major = models.ForeignKey(Major, on_delete=models.PROTECT, null=True)
    nickname = models.CharField(max_length=64, null=True)
    sign = models.CharField(max_length=256, null=True)  # 个性签名
    gender = models.BooleanField(null=True)  # 性别 男性为True
    birthday = models.DateField(null=True)
    birthplace = models.TextField(null=True)
    nationality = models.TextField(null=True)
    avatar_url = models.TextField(null=True)
    experience = models.IntegerField(null=True)  # 用户经验
    token = models.CharField(max_length=36)  # MUST+ token
    coes_cookie = models.TextField(default="")  # COES cookie
    token_expired_time = models.DateTimeField()  # token expired time

    def __str__(self):
        return "%s(%s)" % (self.name_zh, self.student_id)


# 老师
class Teacher(models.Model):
    name_zh = models.CharField(max_length=16)  # 中文名
    name_en = models.CharField(max_length=64)  # 英文名
    faculty = models.ForeignKey(Faculty, on_delete=models.PROTECT)
    avatar_url = models.TextField(default="")  # 头像
    position = models.CharField(max_length=32)  # 职位
    email = models.CharField(max_length=64)  # 电子邮件地址
    office_room = models.TextField(default="")  # 办公室
    office_hour = models.TextField(default="")  # 办公时间

    def __str__(self):
        return self.name_zh
