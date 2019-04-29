from django.db import models


# 部门
class Department(models.Model):
    name = models.CharField(max_length=30)


# 学院
class Faculty(models.Model):
    name = models.CharField(max_length=30)


# 专业
class Major(models.Model):
    name = models.CharField(max_length=30)
    faculty_id = models.ForeignKey(Faculty, on_delete=models.CASCADE)


# 教师
class ClassRoom(models.Model):
    name = models.CharField(max_length=30)


# 通告
class Announcement(models.Model):
    department_id = models.ForeignKey(Department, on_delete=models.PROTECT)  # 来自部门
    faculty_id = models.ForeignKey(Faculty, on_delete=models.PROTECT)  # 来自学院
    title = models.CharField(max_length=128)  # 通知标题
    content = models.TextField()  # 通知内容
    publish_time = models.TimeField()  # 通知发布时间


# 附件
class Attachment(models.Model):
    title = models.CharField(max_length=128)  # 附件标题
    url = models.TextField()  # URL
    belongs_to = models.ForeignKey(Announcement, on_delete=models.CASCADE)  # 属于哪个 Announcement

