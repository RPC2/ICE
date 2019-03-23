from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'learners'

urlpatterns = [
    # TODO: implement this
    # path('<str:username>/view_quiz/', views.ViewQuiz.as_view(), name='viewQuiz'),
    # path('<str:username>/take_quiz/', views.take_quiz, name='takeQuiz'),
    path('view_quiz/', views.view_quiz, name='view_quiz'),
    path('take_quiz/', views.take_quiz, name='take_quiz'),

]