from django.db import models

from Services.Basic.models import Student
from Services.Timetable.models import Course


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
