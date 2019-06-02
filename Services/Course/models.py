from django.db import models

from Services.Basic.models import Faculty, ClassRoom
from Services.Student.models import Student


class Course(models.Model):
    intake = models.IntegerField(default=0)  # 学期
    course_code = models.CharField(max_length=10)  # 课程ID
    course_class = models.CharField(max_length=10)  # 班别
    name_zh = models.CharField(max_length=30)
    name_en = models.CharField(max_length=30)
    name_short = models.CharField(max_length=30)
    credit = models.IntegerField(default=0)
    faculty = models.ForeignKey(Faculty, on_delete=models.PROTECT)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.PROTECT)
    date_start = models.DateField()
    date_end = models.DateField()
    time_start = models.TimeField()
    time_end = models.TimeField()

    def __str__(self):
        return self.course_code + " " + self.name_zh + " " + self.name_en

    class Meta:
        unique_together = (("intake", "course_id", "course_class"),)


class Schedule(models.Model):
    date_start = models.DateField()
    date_end = models.DateField()
    time_start = models.TimeField()
    time_end = models.TimeField()
    day_of_week = models.IntegerField(max_length=3)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.date_start) + " - " + str(self.date_end) + " in " + str(self.classroom)

    class Meta:
        unique_together = (("intake", "course_id", "course_class"),)


# 科目评论
class Comment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.PROTECT)  # 被评论的课程id
    student = models.ForeignKey(Student, on_delete=models.PROTECT)  # 评论发布者id
    thumbs_up = models.IntegerField(default=0)  # 点赞数量
    thumbs_down = models.IntegerField(default=0)  # 点赞数量
    rank = models.IntegerField(default=3)  # 评分
    content = models.TextField()  # 评论正文
    publish_time = models.TimeField()  # 发布时间
    visible = models.BooleanField()  # 是否可见


# 哪个学生认为哪条评论赞
class ThumbsUpComment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    thumbs_time = models.DateTimeField()


# 哪个学生认为哪条评论差
class ThumbsDownComment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    thumbs_time = models.DateTimeField()
