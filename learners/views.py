from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
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
    progress = Progress.objects.get(id=1);
    course = Course.objects.get(slug=slug)
    modules = Module.objects.filter(Course_id=course.id)
    return render(request, 'learner_course_detail.html', {'course': course, 'modules': modules, 'progress': progress.latest_progress})
def module_detail(request, moduleid):
    module = Module.objects.get(id=moduleid)
    progress = Progress.objects.get(id=1);
    components = Component.objects.filter(Module_id=module.id)
    return render(request, 'learner_module_detail.html', {'components': components, 'module': module, 'progress': progress.latest_progress})

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
            # return HttpResponseRedirect('/learner/view_result/')
            return redirect('learners:view_result', module_id=module_id)
    else:
        form = QuizForm(questions=question_list)

    return render(request, 'take_quiz.html', {'form': form})


def view_result(request, module_id):
    progress = Progress.objects.get(id = 1);
    module = Module.objects.get(id=module_id)
    course_id = module.Course_id
    current_order = module.order
    next_module = Module.objects.get(Course_id=course_id, order = current_order+1)
    next_module_id = next_module.id
    latest_submission = QuizResult.objects.get(pk=len(list(QuizResult.objects.all())))
    if latest_submission.total_score >= 10:
        result = "passed"
        progress.latest_progress = progress.latest_progress+1
        progress.save()
    else:
        result = 'failed'
    return render(request, 'quiz_result.html', {'total_score': latest_submission.total_score,
                                                'pass_or_fail': result,
                                                'current_module_id':module_id,
                                                'next_module_id': next_module_id})

