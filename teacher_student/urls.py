from django.urls import path
from .views import teacher_student_list_view

urlpatterns = [
    path('', teacher_student_list_view, name='teacher_student_list'),
]
