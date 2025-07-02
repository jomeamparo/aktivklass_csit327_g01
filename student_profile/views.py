from django.shortcuts import render, redirect
from django.contrib import messages
from core.models import Student, StudentProfile
from .forms import StudentProfileForm, StudentStatusForm

def student_profile_view(request):
    """
    Display and handle updates for the student profile
    """
    # Check if user is logged in using our custom session authentication
    if 'user_id' not in request.session:
        # If not logged in, redirect to login page with next parameter
        return redirect('/?next=/student_profile/')
    
    # Get the logged-in student from the session
    student_id = request.session['user_id']
    student = Student.objects.filter(student_id=student_id).first()
    
    if not student:
        messages.error(request, 'Student not found.')
        return redirect('/')
    
    # Make sure the student has a profile
    profile, created = StudentProfile.objects.get_or_create(student=student)
    
    # Process form submission
    if request.method == 'POST':
        form = StudentProfileForm(
            request.POST, 
            request.FILES, 
            instance=student,
            profile_instance=profile
        )
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was updated successfully!')
            return redirect('student_profile')
    else:
        form = StudentProfileForm(
            instance=student,
            profile_instance=profile
        )

    status_form = StudentStatusForm(initial={'status': student.status})
    
    context = {
        'student': student,
        'profile': profile,
        'form': form,
        'status_form': status_form,
        'completion_percentage': profile.profile_completion_percentage(),
    }
    return render(request, 'student_profile/student_profile.html', context)

def update_student_status(request, student_id):
    """
    Update only the status of a student
    """
    # Check if user is logged in using our custom session authentication
    if 'user_id' not in request.session:
        # If not logged in, redirect to login page with next parameter
        return redirect(f'/?next={request.path}')
    
    # Get the actual student from the database
    student = Student.objects.filter(student_id=student_id).first()
    
    if not student:
        messages.error(request, 'Student not found.')
        return redirect('student_profile')
    
    if request.method == 'POST':
        form = StudentStatusForm(request.POST)
        if form.is_valid():
            student.status = form.cleaned_data['status']
            student.save()
            messages.success(request, 'Student status updated successfully!')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    
    return redirect('student_profile')