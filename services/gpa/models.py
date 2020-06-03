from django.db import models


class GPA(models.Model):
    student = models.ForeignKey('student.Student', on_delete=models.CASCADE)
    intake = models.IntegerField(default=0) # 学期
    total_credit = models.FloatField(default=0) # 学期学分
    pass_credit = models.FloatField(default=0) # 通过学分
    fail_credit = models.FloatField(default=0) # 未通过学分
    gpa_credit = models.FloatField(default=0) # GPA 学分
    gpa = models.FloatField(default=0) # 学期 GPA
    accum_gpa = models.FloatField(default=0) # 累计 GPA
    update_time = models.DateTimeField(auto_now_add=True)  # 最后更新时间