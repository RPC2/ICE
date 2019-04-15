from django import forms
from courses import models
from django.core.files.uploadedfile import SimpleUploadedFile

class SendEmailForm(forms.Form):
    instructor_email = forms.CharField(max_length=50, help_text='Please input instructor email here.')

class SignupForm(forms.Form):
    username= forms.CharField(max_length=30,help_text='Required. Please input your username.')
    password = forms.CharField(max_length=30, help_text='Required. Inform input your password.')
    first_name = forms.CharField(max_length = 30, help_text = 'Required. Please input your first name')
    last_name = forms.CharField(max_length = 30, help_text = 'Required. Please input your last name')
    autobiography = forms.CharField(max_length = 2000, help_text = 'Required. Please input a short autobiography (2000 characters)')


class createCourse(forms.ModelForm):
    class Meta:
        model = models.Course
        fields = ['title', 'description', 'thumb', 'slug', 'category', 'CECU', 'category']

class createModule(forms.ModelForm):
    class Meta:
        model = models.Module
        fields = ['title']


class addComponent(forms.Form):
    def __init__(self, *args, **kwargs):
        # print(kwargs)
        self.courseid = kwargs.pop('courseid')
        # QUESTION_CHOICES = models.QuizQuestion.objects.filter(module_id=self.moduleid)
        COMPONENT_CHOICES = [[x.id, x.title] for x in models.Component.objects.filter(Course_id=self.courseid) if x.Module_id== None ]
        super(addComponent, self).__init__(*args, **kwargs)
        self.fields['components'] = forms.MultipleChoiceField(choices=COMPONENT_CHOICES, required=False,
                                                             widget=forms.CheckboxSelectMultiple())

class createQuiz(forms.Form):
    def __init__(self, *args, **kwargs):
        # print(kwargs)
        self.moduleid = kwargs.pop('moduleid')
        # QUESTION_CHOICES = models.QuizQuestion.objects.filter(module_id=self.moduleid)
        QUESTION_CHOICES = [[x.id, x.question_text] for x in models.QuizQuestion.objects.filter(module_id=self.moduleid) if x.selected==False ]
        super(createQuiz, self).__init__(*args, **kwargs)
        self.fields['questions'] = forms.MultipleChoiceField(choices=QUESTION_CHOICES, required=False,
                                                             widget=forms.CheckboxSelectMultiple())
        self.fields['pass_score'] = forms.IntegerField(min_value=0, max_value=100)
