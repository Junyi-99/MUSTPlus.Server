from django.db import models


# 科目信息
from Services.Basic.models import Faculty, ClassRoom, Student, Teacher


class Course(models.Model):
    course_id = models.CharField(max_length=10)  # 课程ID
    course_class = models.CharField(max_length=10)  # 班别
    name_zh = models.CharField(max_length=30)
    name_en = models.CharField(max_length=30)
    name_short = models.CharField(max_length=30)
    credit = models.IntegerField(default=0)
    faculty_id = models.ForeignKey(Faculty, on_delete=models.PROTECT)
    classroom_id = models.ForeignKey(ClassRoom, on_delete=models.PROTECT)
    date_start = models.DateField()
    date_end = models.DateField()
    time_start = models.TimeField()
    time_end = models.TimeField()

    def __str__(self):
        return self.course_id + " " + self.name_zh

    class Meta:
        unique_together = (("course_id", "course_class"),)


# 老师教什么课
class TeacherTeachCourse(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


# 学生选什么课
class StudentTakeCourse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
