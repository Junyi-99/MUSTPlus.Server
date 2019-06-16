from django.db import models

# 学生
from services.basic.models import Faculty, Program, Major, ClassRoom


class Student(models.Model):
    student_id = models.CharField(max_length=18, primary_key=True)
    name_zh = models.CharField(max_length=16, null=True)
    name_en = models.CharField(max_length=16, null=True)
    nickname = models.CharField(max_length=64, null=True)
    sign = models.CharField(max_length=256, null=True)  # 个性签名
    gender = models.BooleanField(null=True)  # 性别 男性为True
    birthday = models.DateField(null=True)
    birthplace = models.TextField(null=True)
    nationality = models.TextField(null=True)
    avatar_url = models.TextField(null=True)
    experience = models.IntegerField(null=True)  # 用户经验
    token = models.CharField(max_length=36)  # MUST+ token
    coes_token = models.TextField()  # coes org.apache.struts.taglib.html.TOKEN
    coes_cookie = models.TextField(default="")  # coes cookie
    token_expired_time = models.DateTimeField()  # token expired time
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, null=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, null=True)
    major = models.ForeignKey(Major, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "%s(%s)" % (self.name_zh, self.student_id)


# 学生选什么课
class TakeCourse(models.Model):
    intake = models.IntegerField(default=0)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey("course.Course", on_delete=models.CASCADE)
    grade = models.CharField(max_length=16, null=True)
    exam_datetime = models.DateTimeField(null=True)
    exam_classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, null=True)
    exam_seat = models.CharField(max_length=16, null=True)

    def __str__(self):
        return str(self.student) + " Enroll " + str(self.course) + " At " + str(self.intake)

    # class Meta:
    #     unique_together = (("intake", "teacher", "course"),)


# student Login Attempt Records
class LoginRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    time = models.DateTimeField()
    ip = models.CharField(max_length=15)
    state = models.IntegerField(default=0)
    # 0: No meaning，1: Login successful,
    # 2: Login failed (wrong password), 3
    # : Login failed (haven't logout), 4: Login failed (unknown)
