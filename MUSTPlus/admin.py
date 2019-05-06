from django.contrib import admin

from .models import Announcement
from .models import Attachment
from .models import ClassRoom
from .models import CommentCourse
from .models import Course
from .models import Department
from .models import Document
from .models import Faculty
from .models import FTP
from .models import Major
from .models import Student
from .models import Teacher

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
admin.site.register(FTP)