from django.urls import path
from .views import student_view_attendance, student_view_results, student_dashboard, student_attendance_present, student_attendance_absent, student_attendance_all, student_attendance_dashboard, export_attendance_excel, student_results_dashboard, student_attendance_subject_detail

urlpatterns = [
    path('dashboard/', student_dashboard, name='student_dashboard'),
    path('attendance_dashboard/', student_attendance_dashboard, name='student_attendance_dashboard'),
    path('attendance/', student_attendance_all, name='student_attendance'),
    path('attendance/view/', student_attendance_all, name='student_view_attendance'),
    path('attendance/present/', student_attendance_present, name='student_attendance_present'),
    path('attendance/absent/', student_attendance_absent, name='student_attendance_absent'),
    path('attendance/subject_detail/', student_attendance_subject_detail, name='student_attendance_subject_detail'),
    path('results/', student_view_results, name='student_view_results'),
    path('results_dashboard/', student_results_dashboard, name='student_results_dashboard'),
    path('attendance/export/', export_attendance_excel, name='attendance_export_excel'),
]
