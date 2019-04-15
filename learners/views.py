from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required, user_passes_test


from django.template.loader import render_to_string
from .forms import *
from .models import *
from courses.models import *
from courses.forms import *
from learners.models import *
from django.core.mail import send_mail
from django.conf import settings
from django.utils.encoding import force_text,force_bytes
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User,Group
import urllib.request
import json

<<<<<<< HEAD
=======

>>>>>>> 48d2eadf579814b877f0cd42dd80f2ea51bb4c45
def is_member(user):
    return user.groups.filter(name='learner').exists()
staff_id= "00003297"
first_name= "Sid"
last_name= "Miglani"
email= "sidhrmiglani@gmail.com"
def send_email(request):
    if request.method == 'POST':
        form = SendEmailForm(request.POST)
        if form.is_valid():
            global staff_id
            global first_name
            global last_name
            global email
            staff_id = form.cleaned_data.get('staff_id')
            url="https://gibice-hrserver.herokuapp.com/info/"+staff_id
            req = urllib.request.Request(url)
            r = urllib.request.urlopen(req).read()
            cont = json.loads(r.decode('utf-8'))
            first_name=cont['first_name']
            last_name = cont['last_name']
            email=cont['email']
            message = render_to_string('learner_account_activation_email.html', {
                'domain': get_current_site(request).domain,
                'uid': urlsafe_base64_encode(force_bytes(staff_id)),
                'token': account_activation_token.make_token(staff_id),
            })
            send_mail(
                'Activate your account',
                message,
                settings.EMAIL_HOST_USER,
                ['loganwanghk@gmail.com'],
            )
            return redirect('learners:waitforactivation')
    else:
        form =SendEmailForm()
    return render(request, 'learner_signup.html', {'form': form})

def waitforactivation(request):
    return render(request,'waitforactivation.html')

def activate(request, uidb64, token):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user=User.objects.create_user(username=username,password=password,first_name=first_name,last_name=last_name,
                                     email=email)
            learner=Learner.objects.create(username=username,password=password,first_name=first_name,last_name=last_name,
                                     email=email,staff_id=staff_id)
            my_group = Group.objects.get(name='learner')
            my_group.user_set.add(user)
            return redirect('learners:activate_complete')
    else:
        form = SignupForm()
    return render(request, 'learner_activate.html', {'form': form})

def activate_complete(request):
    return render(request, 'learner_activate_complete.html')

@login_required
@user_passes_test(is_member)
def user_center(request):
    return render(request, 'usercenter-base.html')

@login_required
@user_passes_test(is_member)
def active_course(request, category):
    categories = Category.objects.all()
    if category == 'all':
        activecourses = Course.objects.all()
    else:
        activecourses = Course.objects.filter(category=category)
    return render(request, 'usercenter-activecourse.html', {'courses': activecourses, 'categories': categories})

@login_required
def course_detail(request,course_id):
    course = Course.objects.get(id=course_id)
    return render(request, 'learner_course_detail.html', {'course': course})


@user_passes_test(is_member)
def modules(request,course_id):
    current_learner = Learner.objects.get(username=request.user.username)
    course = Course.objects.get(id=course_id)
    learner_progress = Progress.objects.get(learner=current_learner, course=course)
    modules = Module.objects.filter(Course_id=course.id)
    return render(request, 'learner_modules.html', {'course': course, 'modules': modules,
                                                    'progress': learner_progress.latest_progress})

@login_required
@user_passes_test(is_member)
def module_detail(request, moduleid): # TODO: Connect with a better URL
    username = request.user.username
    module = Module.objects.get(id=moduleid)
    course =  module.Course
    progress = Progress.objects.get(learner__username=username, course=course)
    components = Component.objects.filter(Module_id=module.id)
    return render(request, 'learner_module_detail.html', {'components': components,'username':username, 'module': module, 'progress': progress.latest_progress})



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

            return redirect('learners:view_result', module_id=current_module.id)
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
    print(current_course.module_set.all)
    current_module = current_course.module_set.filter(order=learner_progress.latest_progress)[0]

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
    learner_history.completed = True
    learner_history.save()


def view_completed_course(request, username):
    current_learner = Learner.objects.get(username=username)
    course_taken = []
    learner_history = EnrollmentHistory.objects.filter(learner=current_learner, completed=True)
    for i in range(len(learner_history)):
        course_taken.append(learner_history[i].course)
    # print(course_taken)
    return render(request, 'completed_course.html', {'courses': course_taken})

