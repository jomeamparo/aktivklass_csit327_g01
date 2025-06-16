from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Student
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import transaction

# Create your views here.

@login_required
def student_list(request):
    students = Student.objects.all()
    return render(request, 'edit_student_revised/student_list.html', {'students': students})

@login_required
def create_student(request):
    if request.method == 'POST':
        try:
            # Create User account
            username = request.POST.get('student_id')
            password = request.POST.get('password', 'defaultpassword123')  # You might want to generate this
            email = request.POST.get('email')
            
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name')
            )
            
            # Create Student profile
            student = Student.objects.create(
                user=user,
                student_id=username,
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                email=email
            )
            
            messages.success(request, 'Student added successfully!')
            return redirect('edit_student_revised:student_list')
            
        except Exception as e:
            messages.error(request, f'Error adding student: {str(e)}')
            return redirect('edit_student_revised:create_student')
    
    return render(request, 'edit_student_revised/create_student.html')

@login_required
@transaction.atomic
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        try:
            # Update Student information
            student.first_name = request.POST.get('first_name')
            student.last_name = request.POST.get('last_name')
            student.email = request.POST.get('email')
            student.student_id = request.POST.get('student_id')
            student.save()
            
            # Update associated User information
            user = student.user
            user.first_name = student.first_name
            user.last_name = student.last_name
            user.email = student.email
            user.username = student.student_id  # Update username if student_id changes
            user.save()
            
            messages.success(request, 'Student information updated successfully!')
            return redirect('edit_student_revised:student_list')
            
        except Exception as e:
            messages.error(request, f'Error updating student: {str(e)}')
            return render(request, 'edit_student_revised/edit_student.html', {'student': student})
    
    return render(request, 'edit_student_revised/edit_student.html', {'student': student})

@login_required
def toggle_student_status(request, student_id):
    if request.method == 'POST':
        student = get_object_or_404(Student, id=student_id)
        student.is_disabled = not student.is_disabled
        student.save()
        
        return JsonResponse({
            'status': 'success',
            'is_disabled': student.is_disabled,
            'button_text': 'Activate' if student.is_disabled else 'Disable',
            'button_class': 'btn-success' if student.is_disabled else 'btn-danger'
        })
    
    return JsonResponse({'status': 'error'}, status=400)
