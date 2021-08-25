from django.db import models

# Create your models here.

class Covid(models.Model):
    date = models.DateField()
    total_cases = models.IntegerField()
    new_cases = models.IntegerField()
    population = models.IntegerField()
    recovered = models.IntegerField()
    tested = models.IntegerField()
    died = models.IntegerField()