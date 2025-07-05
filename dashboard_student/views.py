from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from core.models import Class, ClassJoinRequest, Enrollment, Student
from django.contrib.auth.decorators import login_required

def dashboard_view(request):
    student_id = request.session.get('user_id')
    student = get_object_or_404(Student, student_id=student_id)
    
    # Get enrollment records for this student
    enrollments = Enrollment.objects.filter(student=student)
    
    # Separate visible and hidden classes based on enrollment
    visible_classes = []
    hidden_classes = []
    
    for enrollment in enrollments:
        if enrollment.enrolled_class.is_archived:
            hidden_classes.append(enrollment)
        else:
            visible_classes.append(enrollment)
    
    print(f'Student: {student}')
    print(f'Visible classes: {[cls.enrolled_class.subject_name for cls in visible_classes]}')
    print(f'Hidden classes: {[cls.enrolled_class.subject_name for cls in hidden_classes]}')
    
    # Get pending join requests
    pending_requests = ClassJoinRequest.objects.filter(
        student=student,
        status='pending'
    ).select_related('class_requested')
    
    context = {
        'role': 'student', 
        'visible_classes': visible_classes,
        'hidden_classes': hidden_classes,
        'student': student,
        'pending_requests': pending_requests,
    }
    return render(request, 'dashboard_student/dashboard.html', context)

def leave_class(request, class_id):
    class_instance = get_object_or_404(Class, id=class_id)
    student_id = request.session.get('user_id')
    student = get_object_or_404(Student, student_id=student_id)
    print('user:: ', class_id, student)
    if request.method == 'POST':
        Enrollment.objects.filter(
            student=student,
            enrolled_class=class_instance
        ).delete()
    
    request.session['user_id'] = student_id
    return redirect('dashboard_student')

def join_class(request):
    if request.method == "POST":
        class_code = request.POST.get('class_code') 
        student_id = request.session.get('user_id')

        if not student_id:
            return JsonResponse({'error': 'You must be logged in as a student to join a class.'}, status=403)

        student = get_object_or_404(Student, student_id=student_id)

        try:
            class_instance = Class.objects.get(class_code=class_code)
        except Class.DoesNotExist:
            return JsonResponse({'error': 'Class code not found.'}, status=404)

        existing_request = ClassJoinRequest.objects.filter(
            student=student,
            class_requested=class_instance,
            status='pending'
        ).first()

        if existing_request:
            return JsonResponse({'error': 'Duplicate request or already added to the class'}, status=403)
        else:
            ClassJoinRequest.objects.create(
                student=student,
                class_requested=class_instance,
                status='pending'
            )
            return JsonResponse({'success': True, 'message': 'Your request has been submitted.'}, status=200)

    return redirect('dashboard_student')

def toggle_archive_view(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id, student__student_id=request.session.get('user_id'))
    enrollment.enrolled_class.is_archived = not enrollment.enrolled_class.is_archived
    enrollment.enrolled_class.save()
    return redirect('dashboard_student')