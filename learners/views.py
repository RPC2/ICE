from django.http import HttpResponseRedirect
from django.shortcuts import get_list_or_404, render
from django.urls import reverse
from django.views import generic

from .models import *
from courses.models import *


def view_quiz(request):
    course = Course.objects.get(title__startswith="Intro")
    module = course.module_set.get(title__startswith="Chapter 1")
    question_list = list(module.quizquestion_set.all())

    choice_list = []
    for i in range(len(question_list)):
        choice_list.append(list(question_list[i].quizchoice_set.all()))

    return render(request, 'take_quiz.html', {'q_list': question_list, 'num_of_question': range(len(question_list)),
                                              'c_list': choice_list})


def take_quiz(request, ):
    learner_progress = 0 # TODO: Find the learner's progress from the username
    quiz_module = learner_progress
    questions = get_list_or_404(QuizQuestion, pk=quiz_module)
    try:
        selected_choice = questions.quizchoice_set.get(pk=request.POST['quizChoice'])
    except (KeyError, QuizChoice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'take_quiz.html', {
            'question': questions,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse('templates:results', args=(QuizQuestion.Module,)))