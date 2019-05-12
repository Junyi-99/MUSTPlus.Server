from django.db import models

from Services.Basic.models import Student


class StudentToken(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    token = models.CharField(max_length=32)
    expired_time = models.DateTimeField()


class StudentLogin(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    time = models.DateTimeField()
    ip = models.CharField(max_length=15)
    state = models.IntegerField(default=0)
    # 0: No meaning，1: Login successful,
    # 2: Login failed (wrong password), 3
    # : Login failed (haven't logout), 4: Login failed (unknown)
