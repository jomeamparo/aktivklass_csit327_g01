from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

def attendance_student_view(request):
    return render(request, 'attendance_student/attendance_student.html')
    

