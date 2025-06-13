from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

def help_and_support_view(request):
    return render(request, 'help_and_support/help_and_support.html')
