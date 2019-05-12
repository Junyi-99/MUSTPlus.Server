from django.contrib import admin

from Services.Basic.models import Department, Faculty, Major, ClassRoom, Student, Teacher
from Services.Comment.models import CommentCourse
from Services.News.models import Document, Announcement, Attachment
from Services.Timetable.models import Course

admin.site.register(Department)
admin.site.register(Faculty)
admin.site.register(Major)
admin.site.register(ClassRoom)
admin.site.register(Document)
admin.site.register(Announcement)
admin.site.register(Attachment)

admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(CommentCourse)
#admin.site.register(FTP)