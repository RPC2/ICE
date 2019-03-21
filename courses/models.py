from django.db import models

# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    open_status = models.BooleanField(default=True)
    thumb = models.ImageField(default='default.png', blank=True)

    def __str__(self):
        return self.title

    def snippet(self):
        return self.description

class Module(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    thumb = models.ImageField(default='default.png', blank=True)
    Course = models.ForeignKey(Course, on_delete=models.CASCADE, default=1)
    def __str__(self):
        return self.title

# either text or image?
class Component(models.Model):
    title = models.CharField(max_length=100)
    text_content = models.TextField()
    image_content = models.ImageField(default='default.png', blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    Module = models.ForeignKey(Module, on_delete=models.CASCADE)

    def __str__(self):
        return self.title