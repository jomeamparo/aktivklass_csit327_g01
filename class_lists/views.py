from django.shortcuts import render, get_object_or_404, redirect
from core.models import Class, Student, Enrollment, ClassJoinRequest
from django.contrib import messages

# class_lists/views.py

def class_list_view(request):
    student_id = request.session.get('user_id')
    student = None

    if student_id:
        student = get_object_or_404(Student, student_id=student_id)

    classes = Class.objects.filter(is_archived=False)
    
    return render(request, 'class_lists/class_list.html', {'classes': classes})



def class_detail_view(request, class_id):
    selected_class = get_object_or_404(Class, id=class_id)
    return render(request, 'class_lists/class_detail.html', {'class': selected_class})

def join_class_view(request, class_id):
    if request.method == 'POST':
        student_id = request.session.get('user_id')
        if not student_id:
            messages.error(request, 'You must be logged in to join a class.')
            return redirect('class_list')
            
        student = get_object_or_404(Student, student_id=student_id)
        selected_class = get_object_or_404(Class, id=class_id)
        
        # Check if there's already a pending request
        existing_request = ClassJoinRequest.objects.filter(
            student=student,
            class_requested=selected_class,
            status='pending'
        ).first()

        if existing_request:
            messages.warning(request, 'You already have a pending request to join this class.')
            return redirect('class_list')
        
        # Create new join request
        ClassJoinRequest.objects.create(
            student=student,
            class_requested=selected_class,
            status='pending'
        )
        messages.success(request, f'Request to join {selected_class.subject_name} ({selected_class.subject_code}) has been submitted.')
        return redirect('dashboard_student')
    
    return redirect('class_list')

# class_lists/views.py
from django.shortcuts import redirect

def archive_class_view(request, class_id):
    if request.method == 'POST':
        selected_class = get_object_or_404(Class, id=class_id)
        selected_class.is_archived = True
        selected_class.save()
        messages.success(request, f"{selected_class.subject_name} has been archived.")
    return redirect('class_list')

