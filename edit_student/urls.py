from django.urls import path
from . import views

urlpatterns = [
    path('edit_student', views.edit_student_view, name='edit_student'),
    path('toggle-student-status/<str:student_id>/', views.toggle_student_status, name='toggle_student_status'),
] 