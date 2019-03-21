from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import Course, Module, Component
from django.contrib.auth.decorators import login_required

def instructor_course_list(request):
    courses = Course.objects.all().order_by('date');
    return render(request, 'courses/course_list.html', { 'courses': courses })

def instructor_modules(request, slug):
    course = Course.objects.get(slug=slug)
    modules = Module.objects.filter(Course_id = course.id)
    return render(request, 'courses/course_detail.html', { 'course': course, 'modules': modules })
def instructor_components(request, id):
    module = Module.objects.get(id=id)
    components = Component.objects.filter(Module_id = module.id)
    return render(request, 'courses/module_detail.html', { 'components': components, 'module': module })
