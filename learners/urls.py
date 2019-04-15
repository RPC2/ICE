from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'learners'

urlpatterns = [
    url(r'^usercenter$', views.user_center, name="usercenter"),
    url(r'^$', views.send_email, name="send_email"),
    url(r'^waitforactivation$', views.waitforactivation, name="waitforactivation"),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^activatecomplete', views.activate_complete, name="activate_complete"),
    url(r'^activecourse/(?P<category>[\w-]+)/$', views.active_course, name="active-course"),
    url(r'^activecourse/(?P<slug>[\w-]+)/$', views.modules, name="modules"),
    url(r'^activecourse/detail/(?P<course_id>[\w-]+)/$', views.course_detail, name="course_detail"),
    url(r'^activecourse/module/(?P<moduleid>[\w-]+)/$', views.module_detail, name="module_detail"),


]

"""url(r'^take_quiz/(?P<course_title>[\w-]+)/(?P<username>[\w-]+)$', views.take_quiz, name='take_quiz'),
    url(r'^view_result/(?P<course_title>[\w-]+)/(?P<username>[\w-]+)$', views.view_result, name='view_result'),"""