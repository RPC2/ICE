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

def send_email(request):
    if request.method == 'POST':
        form = SendEmailForm(request.POST)
        if form.is_valid():
            staff_id = form.cleaned_data.get('staff_id')
            email=Learner.objects.filter(staff_id=staff_id)
            message = render_to_string('learner_account_activation_email.html', {
                'domain': get_current_site(request).domain,
                'uid': urlsafe_base64_encode(force_bytes(staff_id)).decode(),
                'token': account_activation_token.make_token(staff_id),
            })
            send_mail(
                'Activate your account',
                message,
                settings.EMAIL_HOST_USER,
                ['wa201801@163.com'],
            )
            return redirect('learners:waitforactivation')
    else:
        form =SendEmailForm()
    return render(request, 'learner_signup.html', {'form': form})

def waitforactivation(request):
    return render(request,'waitforactivation.html')

def activate(request, uidb64, token):
    return render(request,'learner_activate.html')
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

@login_required
def course_detail(request,slug):
    progress = Progress.objects.get(id=1)
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


"""
@login_required
@user_passes_test(is_member)
@csrf_protect
def take_quiz(request, course_title, username):
    current_learner = Learner.objects.get(username=username)
    current_course = Course.objects.get(title=course_title)
    learner_progress = Progress.objects.get(learner=current_learner, course=current_course).latest_progress
    current_module = current_course.module_set.get(id=learner_progress)
    question_list = list(current_module.quizquestion_set.filter(selected=True))
    is_last_module = False

    if len(current_course.module_set.all()) == learner_progress: # Learner progress = number of modules in this course
        is_last_module = True

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

    return render(request, 'take_quiz.html', {'form': form})


@login_required
@user_passes_test(is_member)
def view_result(request, course_title, username):
    # Get learner, course, and progress
    current_learner = Learner.objects.get(username=username)
    current_course = Course.objects.get(title=course_title)
    learner_progress = Progress.objects.get(learner=current_learner, course=current_course).latest_progress

    # Get module info
    current_module = current_course.module_set.get(id=learner_progress)
    course_id = current_module.Course_id
    current_order = current_module.order
    next_module = Module.objects.get(Course_id=course_id, order = current_order+1)
    next_module_id = next_module.id

    # Get quiz result (pass or fail)
    latest_submission = QuizResult.objects.get(learner=current_learner, course=current_course)
    if latest_submission.total_score >= 10: # TODO: How does instructor set the passing score?
        result = "passed"
        learner_progress.latest_progress = learner_progress.latest_progress+1
        learner_progress.save()
    else:
        result = 'failed'

    # Is the learner passing the last module?
    is_last_module = False
    if len(current_course.module_set.all()) == learner_progress: # Learner progress = number of modules in this course
        is_last_module = True

    return render(request, 'quiz_result.html', {'total_score': latest_submission.total_score,
                                                'pass_or_fail': result,
                                                'current_module_id':current_module.id,
                                                'next_module_id': next_module_id,
                                                'is_last_module': is_last_module})"""
