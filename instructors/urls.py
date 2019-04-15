from django.conf.urls import url
from . import views

app_name = 'instructors'

urlpatterns = [
    url(r'^$', views.instructor_course_list, name="list"),
    url(r'^modules/(?P<course_id>[\w-]+)/$', views.instructor_modules, name="instructor-modules"),
    url(r'^modules/addcourse$', views.add_course, name="instructor-add-course"),
    url(r'^modules/addmodule/(?P<courseid>[\w-]+)/$', views.add_module, name="instructor-add-module"),
    url(r'^module-detail/module(?P<moduleid>[\w-]+)/$', views.instructor_components, name="instructor-module-detail"),
    url(r'^modules/(?P<moduleid>[\w-]+)/addcomponent/$', views.add_component, name="instructor-add-component"),
    url(r'^modules/(?P<moduleid>[\w-]+)/addquiz/$', views.add_quiz, name="instructor-add-quiz"),
    url(r'^modules/(?P<moduleid>[\w-]+)/viewquiz/$', views.instructor_view_quiz, name="instructor-view-quiz"),
]