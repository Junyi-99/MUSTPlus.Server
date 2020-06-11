"""
Hey, PyLint? SHUT UP
"""
from django.contrib import admin


from services.basic.models import Department as basicDepartment
from services.basic.models import Faculty as basicFaculty
from services.basic.models import Major as basicMajor
from services.basic.models import Program as basicProgram
from services.basic.models import ClassRoom as basicClassRoom
from services.course.models import Course, Ftp, Schedule
from services.gpa.models import GPA
from services.lost.models import LostRecord as lostLostRecord
from services.moments.models import Moment, MomentView
from services.setting.models import Setting as settingSetting
from services.news.models import Document, Announcement, Attachment
from services.student.models import Student, TakeCourse, LoginRecord
from services.teacher.models import Teacher, TeachCourse

admin.site.register(basicDepartment)
admin.site.register(basicFaculty)
admin.site.register(basicMajor)
admin.site.register(basicClassRoom)
admin.site.register(basicProgram)
admin.site.register(Document)
admin.site.register(Announcement)
admin.site.register(Attachment)

admin.site.register(Course)
admin.site.register(GPA)
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


admin.site.register(settingSetting)
admin.site.register(lostLostRecord)

