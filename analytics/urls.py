from django.urls import path
from .views import analytics_view, get_faculty_count, get_student_count, get_active_faculty_count, get_faculty_by_status, get_faculty_by_college, get_colleges, get_students_by_course, get_students_by_year, get_courses, get_years, get_account_status_chart_data, get_faculty_college_chart_data, get_student_course_chart_data, get_student_year_chart_data

urlpatterns = [
    path('', analytics_view, name='analytics'),
    path('get_faculty_count/', get_faculty_count, name='get_faculty_count'),
    path('get_student_count/', get_student_count, name='get_student_count'),
    path('get_active_faculty_count/', get_active_faculty_count, name='get_active_faculty_count'),
    path('get_faculty_by_status/', get_faculty_by_status, name='get_faculty_by_status'),
    path('get_faculty_by_college/', get_faculty_by_college, name='get_faculty_by_college'),
    path('get_colleges/', get_colleges, name='get_colleges'),
    path('get_students_by_course/', get_students_by_course, name='get_students_by_course'),
    path('get_students_by_year/', get_students_by_year, name='get_students_by_year'),
    path('get_courses/', get_courses, name='get_courses'),
    path('get_years/', get_years, name='get_years'),
    path('get_account_status_chart_data/', get_account_status_chart_data, name='get_account_status_chart_data'),
    path('get_faculty_college_chart_data/', get_faculty_college_chart_data, name='get_faculty_college_chart_data'),
    path('get_student_course_chart_data/', get_student_course_chart_data, name='get_student_course_chart_data'),
    path('get_student_year_chart_data/', get_student_year_chart_data, name='get_student_year_chart_data'),
]
