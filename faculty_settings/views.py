from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm


def faculty_settings(request):
    context = {
        'role': 'faculty'
    }
    return render(request, 'faculty_settings/faculty_settings.html', context)
