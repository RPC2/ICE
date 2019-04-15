from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from courses.models import Course, Module, Component, QuizQuestion, QuizChoice
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms
def is_member(user):
    return user.groups.filter(name='instructor').exists()

@login_required
@user_passes_test(is_member)
def instructor_course_list(request):
    current_user = request.user
    courses = Course.objects.filter(instructor_user_id=current_user.id).order_by('date');
    # courses = Course.objects.filter(instructor_id=1).order_by('date');
    return render(request, 'instructor_course_list.html', {'courses': courses})


@login_required
@user_passes_test(is_member)
def instructor_modules(request, course_id):
    course = Course.objects.get(id=course_id)
    modules = Module.objects.filter(Course_id = course.id)
    return render(request, 'instructor_module_list.html', {'course': course, 'modules': modules})

@login_required
@user_passes_test(is_member)
def instructor_components(request, moduleid):
    module = Module.objects.get(id=moduleid)
    components = Component.objects.filter(Module_id = module.id)
    return render(request, 'instructor_module_detail.html', {'components': components, 'module': module})

@login_required
@user_passes_test(is_member)
def add_course(request):
    if request.method == 'POST':
        form = forms.createCourse(request.POST,request.FILES)
        if form.is_valid():
            #save course to DB
            instance = form.save(commit=False)
            instance.instructor_user_id = request.user.id
            instance.instructor_id = request.user.id
            instance.save()
            return redirect('instructors:list')
    else:
        form = forms.createCourse()
        return render(request, 'add_course.html', {'form':form})

@login_required
@user_passes_test(is_member)
def add_module(request, courseid):
    if request.method == 'POST':
        form = forms.createModule(request.POST,request.FILES)
        if form.is_valid():
            #save module to DB
            instance = form.save(commit=False)
            course = Course.objects.get(id=courseid)
            order = Module.objects.filter(Course = course).count() + 1
            instance.Course = course
            instance.order = order
            instance.save()
            return redirect('instructors:instructor-modules', course_id=course.id)
    else:
        form = forms.createModule()
        return render(request, 'add_module.html', {'form':form, 'courseid':courseid})

@login_required
@user_passes_test(is_member)
def add_component(request, moduleid):
    module = Module.objects.get(id = moduleid)
    course_id = module.Course_id
    if request.method == 'POST':
        form = forms.addComponent(request.POST,request.FILES, courseid=course_id)
        if form.is_valid():
            #save component to DB
            componentids = form.cleaned_data.get('components')
            for id in componentids:
                component = Component.objects.get(id=id)
                component.Module_id =moduleid
                component.save()
            return redirect('instructors:instructor-module-detail', moduleid=module.id)
    else:
        form = forms.addComponent(courseid=course_id)
        return render(request, 'add_component.html', {'form':form, 'moduleid':moduleid})

@login_required
@user_passes_test(is_member)
def add_quiz(request, moduleid):
    if request.method == 'POST':
        form = forms.createQuiz(request.POST, moduleid= moduleid)
        if form.is_valid():
            #switch selected to True
            questionids = form.cleaned_data.get('questions')
            for id in questionids:
                question = QuizQuestion.objects.get(id=id)
                question.selected = True
                question.save()
            module = Module.objects.get(id=moduleid)
            return redirect('instructors:instructor-module-detail', moduleid=module.id)
    else:
        form = forms.createQuiz(moduleid= moduleid)
        return render(request, 'add_quiz.html', {'form':form, 'moduleid':moduleid})


@login_required
@user_passes_test(is_member)
def instructor_view_quiz(request, moduleid):
    module = Module.objects.get(id=moduleid)
    questions = QuizQuestion.objects.filter(module_id=moduleid);
    # choices = QuizChoice.objects.filter(moduleid_id=moduleid);
    choices = {}
    for question in questions:
        if question.selected == True:
            answers = QuizChoice.objects.filter(question_id = question.id)
            choices[question] = answers

    return render(request, 'instructor_view_quiz.html', {'questions': questions, 'choices': choices, 'module_title':module.title})