<<<<<<< HEAD
from django.shortcuts import render

def help_and_support(request):
    return render(request, 'help_and_support/help_support.html')

# Create your views here.
=======
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

def help_and_support_view(request):
    return render(request, 'help_and_support/help_and_support.html')
>>>>>>> e85a118 (feature(help_and_support): create_help_and_support_ui)
