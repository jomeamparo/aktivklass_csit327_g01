from django.shortcuts import render, redirect
from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from core.models import Student # Import Student from core app
from .forms import StudentProfileForm
from django import forms

class StudentStatusForm(forms.Form):
    status = forms.ChoiceField(choices=[('Available', 'Available'), ('Busy', 'Busy'), ('Offline', 'Offline')])

# @login_required
def student_profile_view(request):
    # Create a dummy student object for static display
    student = type('Student', (object,), {})
    student.student_id = "S001"
    student.first_name = "John"
    student.last_name = "Doe"
    student.email = "john.doe@example.com"
    student.phone_number = "1234567890"
    student.status = "Available"
    student.course = "Computer Science"
    student.year = "2nd Year"

    if request.method == 'POST':
        form = StudentProfileForm(request.POST)
        if form.is_valid():
            student.first_name = form.cleaned_data['first_name']
            student.last_name = form.cleaned_data['last_name']
            student.email = form.cleaned_data['email']
            student.phone_number = form.cleaned_data['phone_number']
            student.status = form.cleaned_data['status']
            student.course = form.cleaned_data['course']
            student.year = form.cleaned_data['year']

            messages.success(request, 'Your profile was updated successfully!')
            return redirect('student_profile') # Redirect to the same page
    else:
        form = StudentProfileForm(initial={
            'student_id': student.student_id,
            'first_name': student.first_name,
            'last_name': student.last_name,
            'email': student.email,
            'phone_number': student.phone_number,
            'status': student.status,
            'course': student.course,
            'year': student.year,
        })

    status_form = StudentStatusForm(initial={'status': student.status})

    context = {
        'student': student,
        'form': form,
        'status_form': status_form,
    }
    return render(request, 'student_profile/student_profile.html', context)

# This function will now update the static student object
def update_student_status(request, student_id):
    # Re-create the static student object to maintain state across requests for demonstration
    student = type('Student', (object,), {})
    student.student_id = "S001"
    student.first_name = "John"
    student.last_name = "Doe"
    student.email = "john.doe@example.com"
    student.phone_number = "1234567890"
    student.status = "Available"
    student.course = "Computer Science"
    student.year = "2nd Year"

    if request.method == 'POST':
        form = StudentStatusForm(request.POST)
        if form.is_valid():
            student.status = form.cleaned_data['status']
            messages.success(request, 'Student status updated successfully!')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    return redirect('student_profile')