from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required, user_passes_test


from .models import *
from courses.models import *
from courses.forms import *
from learners.models import *
def is_member(user):
    return user.groups.filter(name='learner').exists()

@login_required
@user_passes_test(is_member)
def user_center(request):
    return render(request, 'usercenter-base.html')

@login_required
@user_passes_test(is_member)
def active_course(request, category):
    categories = Course.objects.order_by().values_list('category', flat=True).distinct()
    if category == 'all':
        activecourses = Course.objects.all()
    else:
        activecourses = Course.objects.filter(category=category)
    return render(request, 'usercenter-activecourse.html', {'courses': activecourses, 'categories': categories})


@user_passes_test(is_member)
def modules(request,slug):
    progress = Progress.objects.get(id=1);
    course = Course.objects.get(slug=slug)
    modules = Module.objects.filter(Course_id=course.id)
    return render(request, 'learner_modules.html', {'course': course, 'modules': modules, 'progress': progress.latest_progress})

@login_required
@user_passes_test(is_member)
def course_detail(request, course_id):
    course = Course.objects.get(id=course_id)
    return render(request, 'learner_course_detail.html',
                  {'course': course} )

@login_required
@user_passes_test(is_member)
def module_detail(request, moduleid):
    module = Module.objects.get(id=moduleid)
    progress = Progress.objects.get(id=1);
    components = Component.objects.filter(Module_id=module.id)
    return render(request, 'learner_module_detail.html', {'components': components, 'module': module, 'progress': progress.latest_progress})



#@login_required
#@user_passes_test(is_member)
@csrf_protect
def take_quiz(request, course_id, username):
    current_learner = Learner.objects.get(username=username)
    # print(current_learner)
    current_course = Course.objects.get(id=course_id)
    # print(current_course)
    learner_progress = Progress.objects.get(learner=current_learner, course=current_course).latest_progress
    # print(learner_progress)
    current_module = current_course.module_set.get(order=learner_progress)
    # print(current_module.title)
    question_list = list(current_module.quizquestion_set.filter(selected=True))

    if request.method == 'POST':
        form = QuizForm(request.POST or None, questions=question_list)
        total = 0
        if form.is_valid():
            for (question_description, answer) in form.answers():
                choice = QuizChoice.objects.get(choice_text=answer)
                total += choice.value
                quiz_result = QuizResult.objects.get(learner=current_learner, course=current_course)
                quiz_result.total_score = total
                quiz_result.save()

            return redirect('learners:view_result', module_id=module_id)
    else:
        form = QuizForm(questions=question_list)

    #print(course_id)
    #print(username)
    return render(request, 'take_quiz.html', {'form': form,
                                              'course_id': course_id,
                                              'username': username,
                                              })


#@login_required
#@user_passes_test(is_member)
def view_result(request, course_id, username):
    # Get learner, course, and progress
    current_learner = Learner.objects.get(username=username)
    current_course = Course.objects.get(id=course_id)
    learner_progress = Progress.objects.get(learner=current_learner, course=current_course)

    # Get module info
    current_module = current_course.module_set.get(id=learner_progress.latest_progress)
    # print(current_module.title)
    current_order = current_module.order

    # Is the learner taking the quiz of the last module?
    is_last_module = False
    next_module_id = 0
    if len(current_course.module_set.all()) == learner_progress.latest_progress: # Learner progress = number of modules in this course
        is_last_module = True
    else:
        next_module = Module.objects.get(Course_id=course_id, order=current_order + 1)
        next_module_id = next_module.id

    # Get quiz result (pass or fail)
    latest_submission = QuizResult.objects.get(learner=current_learner, course=current_course)
    if latest_submission.total_score >= 10: # TODO: How does instructor set the passing score?
        result = "passed"
        if is_last_module:
            time_now = datetime.datetime.now()
            update_learner_history(username, course_id, time_now)
        else:
            learner_progress.latest_progress = learner_progress.latest_progress + 1
            learner_progress.save()
    else:
        result = 'failed'

    return render(request, 'quiz_result.html', {'total_score': latest_submission.total_score,
                                                'pass_or_fail': result,
                                                'current_module_id':current_module.id,
                                                'next_module_id': next_module_id,
                                                'is_last_module': is_last_module,
                                                })


def update_learner_history(username, course_id, time):
    current_learner = Learner.objects.get(username=username)
    current_course = Course.objects.get(id=course_id)
    learner_history = EnrollmentHistory.objects.get(learner=current_learner, course=current_course)
    learner_history.date_completed = time


def view_completed_course(request, username):
    current_learner = Learner.objects.get(username=username)
    course_taken = []
    learner_history = EnrollmentHistory.objects.filter(learner=current_learner)
    for i in range(len(learner_history)):
        course_taken.append(learner_history[i].course)
    # print(course_taken)
    return render(request, 'completed_course.html', {'courses': course_taken})

