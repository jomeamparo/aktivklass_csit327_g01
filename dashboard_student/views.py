from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from core.models import Class, ClassJoinRequest, Enrollment, Student

def dashboard_view(request):
    student_id = request.session.get('user_id')
    student = get_object_or_404(Student, student_id=student_id)

    # Get enrolled classes from Enrollment table
    enrollments = Enrollment.objects.filter(
        student=student
    ).select_related('enrolled_class')

    enrolled_classes = [enrollment.enrolled_class for enrollment in enrollments]

    context = {
        'role': 'student',
        'classes': enrolled_classes,
        'student': student,
        'fullname': f"{student.first_name} {student.last_name}",
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