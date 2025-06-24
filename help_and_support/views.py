from django.shortcuts import render
from django.shortcuts import render, redirect

def help_and_support(request):
    if 'role' not in request.session:
        return redirect('login')
    
    role = request.session['role'] 

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

def help_and_support_view(request):
    return render(request, 'help_and_support/help_and_support.html')
    # if role == 'admin':
    #     return render(request, 'help_and_support/help_and_support_admin.html', {'role': role}) # No admin html yet
    # if role == 'faculty':
    #     return render(request, 'help_and_support/help_and_support_faculty.html', {'role': role})
    if role == 'student':
        return render(request, 'help_and_support/help_and_support_student.html', {'role': role})
    
    return redirect('login')
