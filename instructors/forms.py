from django import forms
from courses import models

class createModule(forms.ModelForm):
    class Meta:
        model = models.Module
        fields = ['title']

class createComponent(forms.ModelForm):
    class Meta:
        model = models.Component
        fields = ['title', 'text_content', 'image_content']