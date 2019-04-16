from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'learners'

urlpatterns = [

    url(r'^$', views.user_center, name="usercenter"),
    url(r'^activecourse/category/(?P<category>[\w ]+)/$', views.active_course, name="active-course"),
    url(r'^activecourse/(?P<course_id>[\w-]+)/$', views.modules, name="modules"),
    url(r'^activecourse/detail/(?P<course_id>[\w-]+)/$', views.course_detail, name="course_detail"),
    url(r'^activecourse/module/(?P<moduleid>[\w-]+)/$', views.module_detail, name="module_detail"),
    url(r'^activecourse/(?P<course_id>[\w-]+)/take_quiz/(?P<username>[\w-]+)$', views.take_quiz, name='take_quiz'),
    url(r'^activecourse/(?P<course_id>[\w-]+)/view_result/(?P<username>[\w-]+)$', views.view_result,
        name='view_result'),

    url(r'^completed_course/(?P<username>[\w-]+)$', views.view_completed_course)

]

<<<<<<< HEAD
"""url(r'^take_quiz/(?P<course_title>[\w-]+)/(?P<username>[\w-]+)$', views.take_quiz, name='take_quiz'),
    url(r'^view_result/(?P<course_title>[\w-]+)/(?P<username>[\w-]+)$', views.view_result, name='view_result'),"""
=======
>>>>>>> 48d2eadf579814b877f0cd42dd80f2ea51bb4c45
