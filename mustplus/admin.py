"""
Hey, PyLint? SHUT UP
"""
from django.contrib import admin

from services.basic.models import Department, Faculty, Major, Program, ClassRoom
from services.course.models import Course, Ftp, Schedule
from services.moments.models import Moment, MomentView
from services.news.models import Document, Announcement, Attachment
from services.student.models import Student, TakeCourse, LoginRecord
from services.teacher.models import Teacher, TeachCourse

admin.site.register(Department)
admin.site.register(Faculty)
admin.site.register(Major)
admin.site.register(ClassRoom)
admin.site.register(Document)
admin.site.register(Announcement)
admin.site.register(Attachment)

admin.site.register(Course)
admin.site.register(Ftp)
admin.site.register(Schedule)
#admin.site.register(Comment)

admin.site.register(Moment)
admin.site.register(MomentView)

admin.site.register(Student)
admin.site.register(TakeCourse)
admin.site.register(LoginRecord)
admin.site.register(Teacher)
admin.site.register(TeachCourse)
# admin.site.register(FTP)

