from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from core.models import Student, Class, Attendance, Grade, Activity
 
from django.shortcuts import render
from core.models import Student, Class, Attendance, Grade, Activity

def attendance_student_view(request):
    # If the user is logged in and is a student, show their data
    if request.user.is_authenticated and hasattr(request.user, 'student'):
        student = request.user.student
        attendance_records = Attendance.objects.filter(student=student)
        summary = {
            'present': attendance_records.filter(status='Present').count(),
            'absent': attendance_records.filter(status='Absent').count(),
            'late': attendance_records.filter(status='Late').count(),
        }
        recent_feedback = Grade.objects.filter(student=student).exclude(feedback__isnull=True).order_by('-date_graded')[:5]
    else:
        # For anonymous users, show empty or demo data
        summary = {'present': 0, 'absent': 0, 'late': 0}
        recent_feedback = []

    # Determine role and fullname for navbar/header
    if request.user.is_authenticated and hasattr(request.user, 'student'):
        role = 'student'
        fullname = f"{request.user.student.first_name} {request.user.student.last_name}"
    else:
        role = 'guest'
        fullname = 'Guest'

    return render(request, 'attendance_student/attendance_student.html', {
        'summary': summary,
        'recent_feedback': recent_feedback,
        'role': role,
        'fullname': fullname,
    })