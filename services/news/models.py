from django.db import models

from services.basic.models import Department, Faculty
# Banners （适用于 APP 端的 `资讯` 栏目）
from services.student.models import Student


class Banner(models.Model):
    title = models.CharField(max_length=64)  # Banner 标题
    img = models.TextField()  # Banner 图像 URL
    url = models.TextField()  # Banner 链接
    publish_time = models.DateTimeField()  # 发布时间
    visible = models.BooleanField(default=True)


# 文件（适用于 downContent ）
class Document(models.Model):
    title = models.CharField(max_length=128)  # 文件标题
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)  # 来自部门
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, null=True)  # 来自学院
    publish_time = models.DateField()  # 通知发布时间
    url = models.TextField()  # URL
    visible = models.BooleanField(default=True)  # 是否可见

    def __str__(self):
        return self.title


class DocumentViewed(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    view_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.student) + ' viewed ' + str(self.document)


# 通告（适用于 viewContent ）
class Announcement(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)  # 来自部门
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, null=True)  # 来自学院
    title = models.CharField(max_length=128)  # 通知标题
    content = models.TextField()  # 通知内容
    publish_time = models.DateField()  # 通知发布时间
    visible = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class AnnouncementViewed(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    view_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.student) + ' viewed ' + str(self.announcement)


# 附件(适用于 viewContent中的附件)
class Attachment(models.Model):
    title = models.CharField(max_length=128)  # 附件标题
    url = models.TextField()  # URL
    belongs_to = models.ForeignKey(Announcement, on_delete=models.CASCADE)  # 属于哪个 Announcement

    def __str__(self):
        return self.title
