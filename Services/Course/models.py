from django.db import models
from django.utils import timezone


class Course(models.Model):
    course_code = models.CharField(max_length=32)  # 课程ID
    course_class = models.CharField(max_length=32)  # 班别
    name_zh = models.TextField()
    name_en = models.TextField(null=True)
    name_short = models.CharField(max_length=30, null=True)
    credit = models.CharField(max_length=8, null=True)
    faculty = models.ForeignKey("Basic.Faculty", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.course_code + " " + self.name_zh

    class Meta:
        unique_together = (("course_code", "course_class"),)


class Schedule(models.Model):
    intake = models.IntegerField(default=0)  # 学期
    date_begin = models.DateField()
    date_end = models.DateField()
    time_begin = models.TimeField()
    time_end = models.TimeField()
    day_of_week = models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    classroom = models.ForeignKey("Basic.ClassRoom", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.date_begin) + " - " + str(self.date_end) + " in " + str(self.classroom)


# 科目评论
class CourseComment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # 被评论的课程id
    student = models.ForeignKey("Student.Student", on_delete=models.CASCADE)  # 评论发布者id
    thumbs_up = models.IntegerField(default=0)  # 点赞数量
    thumbs_down = models.IntegerField(default=0)  # 点赞数量
    rank = models.IntegerField(default=3)  # 评分
    content = models.TextField()  # 评论正文
    publish_time = models.TimeField(default=timezone.now)  # 发布时间
    visible = models.BooleanField()  # 是否可见


# 哪个学生认为哪条评论赞
class ThumbsUpCourseComment(models.Model):
    student = models.ForeignKey("Student.Student", on_delete=models.CASCADE)
    comment = models.ForeignKey(CourseComment, on_delete=models.CASCADE)
    thumbs_time = models.DateTimeField(default=timezone.now)


# 哪个学生认为哪条评论差
class ThumbsDownCourseComment(models.Model):
    student = models.ForeignKey("Student.Student", on_delete=models.CASCADE)
    comment = models.ForeignKey(CourseComment, on_delete=models.CASCADE)
    thumbs_time = models.DateTimeField(default=timezone.now)
