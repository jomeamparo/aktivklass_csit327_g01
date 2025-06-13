from django.urls import path
from .views import admin_student_list_view, toggle_student_status

urlpatterns = [
    path('', admin_student_list_view, name='student_list_view'),
    path('toggle-student-status/<str:student_id>/', toggle_student_status, name='toggle_student_status'),
]
