from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from courses.models import Course, Module, Component, QuizQuestion, QuizChoice
from django.contrib.auth.decorators import login_required
from . import forms

def instructor_course_list(request):
    current_user = request.user
    # courses = Course.objects.filter(instructor_id = current_user.id).order_by('date');
    courses = Course.objects.filter( instructor_id=1).order_by('date');
    print(courses)
    return render(request, 'instructor_course_list.html', {'courses': courses})

def instructor_modules(request, slug):
    course = Course.objects.get(slug=slug)
    modules = Module.objects.filter(Course_id = course.id)
    return render(request, 'instructor_module_list.html', {'course': course, 'modules': modules})
def instructor_components(request, moduleid):
    module = Module.objects.get(id=moduleid)
    components = Component.objects.filter(Module_id = module.id)
    return render(request, 'instructor_module_detail.html', {'components': components, 'module': module})
def add_module(request, courseid):
    if request.method == 'POST':
        form = forms.createModule(request.POST,request.FILES)
        if form.is_valid():
            #save module to DB
            instance = form.save(commit=False)
            course = Course.objects.get(id=courseid)
            instance.Course = course
            instance.save()
            return redirect('instructors:instructor-modules', slug=course.slug)
    else:
        form = forms.createModule()
        return render(request, 'add_module.html', {'form':form, 'courseid':courseid})

def add_component(request, moduleid):
    if request.method == 'POST':
        form = forms.createComponent(request.POST,request.FILES)
        if form.is_valid():
            #save component to DB
            instance = form.save(commit=False)
            module = Module.objects.get(id=moduleid)
            instance.Module = module
            print("herer")
            print(instance.image_content)
            instance.save()
            return redirect('instructors:instructor-module-detail', moduleid=module.id)
    else:
        form = forms.createComponent()
        return render(request, 'add_component.html', {'form':form, 'moduleid':moduleid})

def add_quiz(request, moduleid):
    if request.method == 'POST':
        form = forms.createQuiz(request.POST, moduleid= moduleid)
        if form.is_valid():
            #switch selected to True
            print(form.cleaned_data.get('questions'))
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

def instructor_view_quiz(request, moduleid):
    questions = QuizQuestion.objects.filter(module_id=moduleid);
    # choices = QuizChoice.objects.filter(moduleid_id=moduleid);
    choices = {}
    for question in questions:
        if question.selected == True:
            answers = QuizChoice.objects.filter(question_id = question.id)
            choices[question] = answers

    print(choices)
    return render(request, 'instructor_view_quiz.html', {'questions': questions, 'choices': choices})