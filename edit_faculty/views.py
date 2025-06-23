from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

def edit_faculty_view(request):
    return render(request, 'edit_faculty/edit_faculty.html', {'form': form})
