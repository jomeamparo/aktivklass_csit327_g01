from django.shortcuts import render, redirect
from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from .models import Student
from .forms import StudentProfileForm

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

    if request.method == 'POST':
        form = StudentProfileForm(request.POST)
        if form.is_valid():
            # Update the dummy object with cleaned data
            student.first_name = form.cleaned_data['first_name']
            student.last_name = form.cleaned_data['last_name']
            student.email = form.cleaned_data['email']
            student.phone_number = form.cleaned_data['phone_number']
            student.status = form.cleaned_data['status']

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
        })

    context = {
        'student': student,
        'form': form
    }
    return render(request, 'student_profile/student_profile.html', context)