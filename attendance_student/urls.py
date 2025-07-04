from django.urls import path
from .views import (
    student_dashboard,
    student_attendance_dashboard,
    student_attendance_subject_detail,
    student_attendance_all,
    export_attendance_excel,
    student_results_dashboard,
    results_subject_detail
)

urlpatterns = [
    # General Student Dashboard
    path('dashboard/', student_dashboard, name='student_dashboard'),

    # --- Attendance URLs ---
    path('attendance/', student_attendance_dashboard, name='student_attendance_dashboard'),
    path('attendance/class/<int:class_id>/', student_attendance_subject_detail, name='student_attendance_subject_detail'),
    path('attendance/all/', student_attendance_all, name='student_attendance_all'),
    path('attendance/export/', export_attendance_excel, name='export_attendance_excel'),

    # --- Results URLs ---
    path('results/', student_results_dashboard, name='student_results_dashboard'),
    path('results/class/<int:class_id>/', results_subject_detail, name='results_subject_detail'),
]