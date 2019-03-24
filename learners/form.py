from django import forms


class QuizForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        super(QuizForm, self).__init__(*args, **kwargs)

        for i, question in enumerate(questions):
            self.fields['question_%s' % i] = forms.ChoiceField(label=question.question_text,
                                                               choices=question.quizchoice_set.all(),
                                                               widget=forms.RadioSelect)