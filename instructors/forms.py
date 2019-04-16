from django import forms
from courses import models
from django.core.files.uploadedfile import SimpleUploadedFile


class createCourse(forms.ModelForm):
    class Meta:
        model = models.Course
        fields = ['title', 'description', 'thumb', 'slug', 'category', 'CECU']

class createModule(forms.ModelForm):
    class Meta:
        model = models.Module
        fields = ['title']

class createComponent(forms.ModelForm):
    class Meta:
        model = models.Component
        fields = ['title', 'text_content', 'image_content']



class createQuiz(forms.Form):
    def __init__(self, *args, **kwargs):
        # print(kwargs)
        self.moduleid = kwargs.pop('moduleid')
        # QUESTION_CHOICES = models.QuizQuestion.objects.filter(module_id=self.moduleid)
        QUESTION_CHOICES = [[x.id, x.question_text] for x in models.QuizQuestion.objects.filter(module_id=self.moduleid) if x.selected==False ]
        super(createQuiz, self).__init__(*args, **kwargs)
        self.fields['questions'] = forms.MultipleChoiceField(choices=QUESTION_CHOICES, required=False,
                                                             widget=forms.CheckboxSelectMultiple())
