from django import forms
from courses import models
from django.core.files.uploadedfile import SimpleUploadedFile

class createModule(forms.ModelForm):
    class Meta:
        model = models.Module
        fields = ['title']

class createComponent(forms.ModelForm):
    class Meta:
        model = models.Component
        fields = ['title', 'text_content', 'image_content']

class createComponent(forms.ModelForm):
    class Meta:
        model = models.Component
        fields = ['title', 'text_content', 'image_content']

class createQuiz(forms.ModelForm):
    class Meta:
        model = models.Component
        fields = ['title', 'text_content', 'image_content']