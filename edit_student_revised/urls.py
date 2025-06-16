from django.urls import path
from . import views

app_name = 'edit_student_revised'

urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('create/', views.create_student, name='create_student'),
    path('edit/<int:student_id>/', views.edit_student, name='edit_student'),
    path('toggle-status/<int:student_id>/', views.toggle_student_status, name='toggle_student_status'),
] 