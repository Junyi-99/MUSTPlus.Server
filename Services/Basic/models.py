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

