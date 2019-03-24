from django.http import HttpResponseRedirect
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse
from django.views import generic


from .models import *
from courses.models import *
from courses.forms import *
from learners.models import *


@csrf_protect
def take_quiz(request):
    module = get_object_or_404(Module, title__startswith="Chapter 1")
    question_list = list(module.quizquestion_set.all())

    if request.method == 'POST':
        form = QuizForm(request.POST or None, questions=question_list)
        total = 0
        if form.is_valid():
            for (question_description, answer) in form.answers():
                choice = QuizChoice.objects.get(choice_text=answer)
                total += choice.value
                QuizResult.objects.create(total_score=total)
            return HttpResponseRedirect('/learner/view_result/')
    else:
        form = QuizForm(questions=question_list)

    return render(request, 'take_quiz.html', {'form': form})


def view_result(request):
    latest_submission = QuizResult.objects.get(pk=len(list(QuizResult.objects.all())))
    if latest_submission.total_score >= 10:
        result = "passed"
    else:
        result = 'failed'
    return render(request, 'quiz_result.html', {'total_score': latest_submission.total_score,
                                                'pass_or_fail': result})
