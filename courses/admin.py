from django.contrib import admin
from .models import Course, Module, Component, QuizChoice, QuizQuestion

admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Component)
admin.site.register(QuizChoice)
admin.site.register(QuizQuestion)