from django.db import models


class Moment(models.Model):
    student = models.ForeignKey('student.Student', on_delete=models.CASCADE)
    forwarding = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    content = models.TextField()
    thumbs_up = models.IntegerField()
    publish_time = models.DateTimeField()
    visible = models.BooleanField()
    pics = models.TextField()  # 用 JSON 存 图片信息，最多9张，[{id,path}]


class Comment(models.Model):
    moment = models.ForeignKey('moments.Moment', on_delete=models.CASCADE)
    student = models.ForeignKey('student.Student', related_name='%(app_label)s_%(class)s_related',
                                related_query_name='%(app_label)s_%(class)ss', on_delete=models.CASCADE)
    forwarding = models.ForeignKey('self', on_delete=models.CASCADE, null=True)  # 评论某评论（只允许二级评论）
    content = models.TextField()
    publish_time = models.DateTimeField()
    visible = models.BooleanField()


class ThumbsUp(models.Model):
    moment = models.ForeignKey('moments.Moment', on_delete=models.CASCADE)
    student = models.ForeignKey('student.Student', related_name='%(app_label)s_%(class)s_related',
                                related_query_name='%(app_label)s_%(class)ss', on_delete=models.CASCADE)
    thumbs_time = models.DateTimeField()


# 记录学生查看校友圈详情
class MomentView(models.Model):
    moment = models.ForeignKey('moments.Moment', on_delete=models.CASCADE)
    student = models.ForeignKey('student.Student', related_name='%(app_label)s_%(class)s_related',
                                related_query_name='%(app_label)s_%(class)ss', on_delete=models.CASCADE)
