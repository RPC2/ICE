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

