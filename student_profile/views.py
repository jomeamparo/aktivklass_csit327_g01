from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

def student_profile_view(request):
    return render(request, 'student_profile/student_profile')