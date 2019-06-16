from django.db import models


# 部门
class Department(models.Model):
    name_zh = models.CharField(max_length=32, primary_key=True)
    name_en = models.CharField(max_length=64, default='unspecified')

    def __str__(self):
        return self.name_zh


# 学院
class Faculty(models.Model):
    name_zh = models.CharField(max_length=32, primary_key=True)
    name_en = models.CharField(max_length=64, default='unspecified')

    def __str__(self):
        return self.name_zh


# 课程
class Program(models.Model):
    name_zh = models.CharField(max_length=128, primary_key=True)
    name_en = models.CharField(max_length=128, default='unspecified')
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return self.name_zh


# 专业
class Major(models.Model):
    name_zh = models.CharField(max_length=32, primary_key=True)
    name_en = models.CharField(max_length=64, default='unspecified')
    program = models.ForeignKey(Program, on_delete=models.CASCADE)  # belongs to which faculty

    def __str__(self):
        return self.name_zh


# 教室
class ClassRoom(models.Model):
    name_zh = models.CharField(max_length=32, primary_key=True)
    name_en = models.CharField(max_length=64, default='unspecified')

    def __str__(self):
        return self.name_zh
