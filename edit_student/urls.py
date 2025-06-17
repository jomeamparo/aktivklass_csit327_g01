from django.urls import path
from . import views

urlpatterns = [
    path('edit/<str:student_id>/', views.edit_student_view, name='edit_student'),
    path('update/<str:student_id>/', views.update_student, name='update_student'),
] 