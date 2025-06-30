from django.urls import path
from faculty_attendance.views import faculty_attendance_view

urlpatterns = [
    path('', faculty_attendance_view, name='faculty_attendance'),
]
