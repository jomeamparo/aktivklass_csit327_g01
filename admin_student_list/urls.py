from django.urls import path
from .views import admin_student_list_view

urlpatterns = [
    path('', admin_student_list_view, name='student_list_view'),
]
