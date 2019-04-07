from django.db import models
from courses.models import *
# Create your models here.

class Learner(models.Model):
    username = models.CharField(max_length=100)
    staff_id = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    last_quiz_result = models.IntegerField(default=0)

    def __str__(self):
        return self.username


class QuizResult(models.Model):
    total_score = models.IntegerField(default=0)
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.learner.username + " scored " + self.total_score + " in the latest quiz of " + self.course.title



