from django.db import models


class Moment(models.Model):
    student = models.ForeignKey('student.Student', on_delete=models.CASCADE)
    forwarding = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    content = models.TextField()
    thumbs_up = models.IntegerField()
    publish_time = models.DateTimeField()
    visible = models.BooleanField()


class Pics(models.Model):
    pic = models.TextField()  # 图片地址
    moment = models.ForeignKey(Moment, on_delete=models.CASCADE)


class MomentComment(models.Model):
    moment = models.ForeignKey(Moment, on_delete=models.CASCADE)
    student = models.ForeignKey('student.Student', on_delete=models.CASCADE)
    forwarding = models.ForeignKey('self', on_delete=models.CASCADE, null=True)  # 评论某评论（只允许二级评论）
    content = models.TextField()
    publish_time = models.DateTimeField()
    visible = models.BooleanField()


class ThumbsUpMomentComment(models.Model):
    student = models.ForeignKey('student.Student', on_delete=models.CASCADE)
    moment = models.ForeignKey(Moment, on_delete=models.CASCADE)
    thumbs_time = models.DateTimeField()
