from django.db import models

from services.student.models import Student

class LostRecord(models.Model):
    student = models.ForeignKey('student.Student', on_delete=models.CASCADE)
    content = models.TextField()
    status = models.TextField() # 直接文本形式存状态，空间浪费就浪费，这样写起来最快
    publish_time = models.DateTimeField()
    visible = models.BooleanField()


    def __str__(self):
        return str(self.id) + ' ' + self.student.name_zh + ' ' + str(self.content)[:30]
