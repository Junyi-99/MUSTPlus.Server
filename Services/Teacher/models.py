from django.db import models

from Services.Basic.models import Faculty



# 老师
from Services.Course.models import Course


class Teacher(models.Model):
    name_zh = models.CharField(max_length=16)  # 中文名
    name_en = models.CharField(max_length=64, default='unspecified')  # 英文名
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    avatar_url = models.TextField(default="")  # 头像
    position = models.CharField(max_length=32)  # 职位
    email = models.CharField(max_length=64)  # 电子邮件地址
    office_room = models.TextField(default="")  # 办公室
    office_hour = models.TextField(default="")  # 办公时间

    def __str__(self):
        return self.name_zh


# 老师教什么课
class TeachCourse(models.Model):
    intake = models.IntegerField(default=0)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.teacher) + " Teach " + str(self.course) + " At " + str(self.intake)

    # class Meta:
    #     unique_together = (("intake", "teacher", "course"),)
