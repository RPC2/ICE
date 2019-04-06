from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'learners'

urlpatterns = [
    # TODO: implement this
    # path('<str:username>/view_quiz/', views.ViewQuiz.as_view(), name='viewQuiz'),
    # path('<str:username>/take_quiz/', views.take_quiz, name='takeQuiz'),

    url(r'^$', views.user_center, name="usercenter"),
    url(r'^activecourse$', views.active_course, name="active-course"),
    url(r'^activecourse/(?P<slug>[\w-]+)/$', views.course_detail, name="course_detail"),
    url(r'^activecourse/module/(?P<moduleid>[\w-]+)/$', views.module_detail, name="module_detail"),
    url(r'^take_quiz/(?P<module_id>[\w-]+)/$', views.take_quiz, name='take_quiz'),
    # path('view_result/', views.view_result, name='view_result'),
    url(r'^view_result/(?P<module_id>[\w-]+)/$', views.view_result, name='view_result'),


]