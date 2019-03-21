from django.conf.urls import url
from . import views

app_name = 'courses'

urlpatterns = [
    url(r'^instructor$', views.instructor_course_list, name="list"),
    url(r'^instructor/modules/(?P<slug>[\w-]+)/$', views.instructor_modules, name="instructor-modules"),
    url(r'^instructor/components/(?P<id>[\w-]+)/$', views.instructor_components, name="instructor-components"),
]