from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
    

def faculty_settings_view(request):

    return render(request, 'faculty_settings/faculty_settings.html')
