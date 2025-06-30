from django.urls import path
<<<<<<< HEAD
from . import views

app_name = 'faculty_attendance'

urlpatterns = [
    path('', views.faculty_attendance_view, name='faculty_attendance'),
    path('history/', views.attendance_history, name='attendance_history'),
    path('mark-time-out/<int:attendance_id>/', views.mark_time_out, name='mark_time_out'),
=======
from .views import faculty_attendance_view

urlpatterns = [
    path('', faculty_attendance_view, name='faculty_attendance'),
>>>>>>> 441be09 (added feature student_attendance)
]
