from django.db import models

class Bordergate(models.Model):
    name = models.CharField(max_length=12) # gate name
    time = models.DateTimeField(auto_now_add=True)
    population = models.IntegerField()