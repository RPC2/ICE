from django.http import HttpResponseRedirect
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse
from django.views import generic


from .models import *
from courses.models import *
from courses.forms import *
from learners.models import *


def user_center(request):
    return render(request, 'usercenter-base.html')
def active_course(request):
    activecourses = Course.objects.all()
    return render(request, 'usercenter-activecourse.html', {'courses': activecourses})
def course_detail(request,slug):
    course = Course.objects.get(slug=slug)
    modules = Module.objects.filter(Course_id=course.id)
    return render(request, 'learner_course_detail.html', {'course': course, 'modules': modules})
def module_detail(request, moduleid):
    module = Module.objects.get(id=moduleid)
    components = Component.objects.filter(Module_id=module.id)
    return render(request, 'learner_module_detail.html', {'components': components, 'module': module})

@csrf_protect
def take_quiz(request,module_id):
    # module = get_object_or_404(Module, title__startswith="Chapter 1")
    module = Module.objects.get(id=module_id)
    question_list = list(module.quizquestion_set.filter(selected=True))

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

