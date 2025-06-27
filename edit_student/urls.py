from django.urls import path
from .views import edit_student_view

urlpatterns = [
    path('', edit_student_view, name='edit_student')
] 