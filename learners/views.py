from django.http import HttpResponseRedirect
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import *
from courses.models import *
from learners.models import *


def view_quiz(request):
    module = get_object_or_404(Module, title__startswith="Chapter 1")
    question_list = list(module.quizquestion_set.all())

    choice_list = []
    for i in range(len(question_list)):
        choice_list.append(list(question_list[i].quizchoice_set.all()))

    return render(request, 'take_quiz.html', {'q_list': question_list, 'num_of_question': range(len(question_list)),
                                              'c_list': choice_list})


def take_quiz(request):
    module = get_object_or_404(Module, title__startswith="Chapter 1")
    question_list = list(module.quizquestion_set.all())

    print("Hi there")

    total = 0

    for q in question_list:
        selected_choice = q.quizchoice_set.get(pk=request.POST['choice'])
        score = selected_choice.value
        total += score

    quiz_result = QuizResult.objects.create(total_score = total)
    print(total)
    return HttpResponseRedirect('learners:view_result')


def view_result(request):
    latest_submission = QuizResult.objects.get(pk=len(list(QuizResult.objects.all())))
    if latest_submission.total_score > 10:
        result = "passed"
    else:
        result = 'failed'
    return render(request, 'quiz_result.html', {'total_score': latest_submission.total_score,
                                                'pass_or_fail': result})
