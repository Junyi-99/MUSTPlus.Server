from django.db import models

from services.basic.models import Faculty
# 老师
from services.course.models import Course


class Teacher(models.Model):
    name_zh = models.CharField(max_length=64, primary_key=True)  # 中文名
    name_en = models.CharField(max_length=64, default='unspecified')  # 英文名
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, null=True)
    avatar_url = models.TextField(default='', null=True)  # 头像
    position = models.CharField(max_length=32, null=True)  # 职位
    email = models.CharField(max_length=64, null=True)  # 电子邮件地址
    office_room = models.TextField(default='', null=True)  # 办公室
    office_hour = models.TextField(default='', null=True)  # 办公时间

    def __str__(self):
        return self.name_zh


# 老师教什么课
class TeachCourse(models.Model):
    intake = models.IntegerField(default=0)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.teacher) + ' Teach ' + str(self.course) + ' At ' + str(self.intake)

    # class Meta:
    #     unique_together = (('intake', 'teacher', 'course'),)
