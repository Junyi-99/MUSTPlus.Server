
from django.contrib import admin

from Services.Basic.models import Department, Faculty, Major, ClassRoom
from Services.News.models import Document, Announcement, Attachment


admin.site.register(Department)
admin.site.register(Faculty)
admin.site.register(Major)
admin.site.register(ClassRoom)
admin.site.register(Document)
admin.site.register(Announcement)
admin.site.register(Attachment)


# admin.site.register(FTP)
