from django.db import models
from services.student.models import Student


# 通告（适用于 viewContent ）
class Setting(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)

    nt_score = models.BooleanField(default=True)  # Notification 成绩查询提醒
    nt_academic = models.BooleanField(default=True)  # Notification 学院通知
    nt_cet = models.BooleanField(default=True)  # Notification 四六级抢考位提醒
    nt_dormitory = models.BooleanField(default=True)  # Notification 宿舍确认提醒
    nt_course = models.BooleanField(default=True)  # Notification 上课提醒
    nt_course_registration = models.BooleanField(default=True)  # Notification 选课提醒
    nt_book_return = models.BooleanField(default=True)  # Notification 还书提醒
    nt_book_borrow = models.BooleanField(default=True)  # Notification 借书提醒
    nt_study_room = models.BooleanField(default=True)  # Notification 自习室预定通知
    nt_catastrophe = models.BooleanField(default=True)  # Notification 自然灾害提醒
    nt_others = models.TextField(default='') # 其他提醒类设置



    def __str__(self):
        return self.student.name_zh + " Settings"
