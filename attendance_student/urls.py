from django.urls import path
from .views import attendance_student_view

urlpatterns = [
    path('', attendance_student_view, name = 'attendance_student')
]