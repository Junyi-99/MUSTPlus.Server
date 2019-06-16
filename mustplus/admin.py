"""
Hey, PyLint? SHUT UP
"""
from django.contrib import admin

from services.basic.models import Department, Faculty, Major, ClassRoom
from services.news.models import Document, Announcement, Attachment

admin.site.register(Department)
admin.site.register(Faculty)
admin.site.register(Major)
admin.site.register(ClassRoom)
admin.site.register(Document)
admin.site.register(Announcement)
admin.site.register(Attachment)


# admin.site.register(FTP)
