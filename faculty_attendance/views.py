from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

def faculty_attendance_view(faculty_attendance):
    return render(faculty_attendance, 'faculty_attendance/faculty_attendance.html')
