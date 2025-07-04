from django.urls import path
from .views import analytics_view, get_faculty_count, get_student_count

urlpatterns = [
    path('', analytics_view, name='analytics'),
    path('get_faculty_count/', get_faculty_count, name='get_faculty_count'),
    path('get_student_count/', get_student_count, name='get_student_count'),
]
