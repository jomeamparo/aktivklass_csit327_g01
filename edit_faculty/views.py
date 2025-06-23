from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from core.models import Faculty

def edit_faculty_view(request):
    facultyList = Faculty.objects.all()
    return render(request, 'edit_faculty/edit_faculty.html', {'facultyList': facultyList})
