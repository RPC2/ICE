from django.db import models

# Create your models here.

class Learner(models.Model):
    username = models.CharField(max_length=100)
    staff_id = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    last_quiz_result = models.IntegerField(default=0)
    last_quiz_result = models.IntegerField(default=0)
