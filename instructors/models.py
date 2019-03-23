from django.db import models

# Create your models here.
class Instructor(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    self_intro = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    thumb = models.ImageField(default='default.png', blank=True)

    def __str__(self):
        return self.username