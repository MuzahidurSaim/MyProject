# grader/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('enter_correct_answers/', views.enter_correct_answers, name='enter_correct_answers'),
    path('enter_num_students/', views.enter_num_students, name='enter_num_students'),
    path('enter_student_answers/', views.enter_student_answers, name='enter_student_answers'),
    path('show_results/', views.show_results, name='show_results'),
]
