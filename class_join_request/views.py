from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from collections import defaultdict

from core.models import Class, ClassJoinRequest, Enrollment, Faculty


def class_join_request_view(request):
    # Get faculty_id from session
    faculty_id = request.session.get('user_id')
    print('faculty_id:: ', faculty_id)
    if not faculty_id:
        messages.error(request, 'Faculty authentication required')
        return redirect('login')  # or your login route

    faculty = Faculty.objects.get(faculty_id=faculty_id)

    # Get all classes taught by this faculty
    classes = Class.objects.filter(faculty=faculty).order_by('subject_name')
    print(f'Faculty {faculty.first_name} teaches {classes.count()} classes: {[c.subject_name for c in classes]}')

    # Prepare a mapping of each class to its join requests
    class_join_requests_map = defaultdict(list)

    for class_obj in classes:
        join_requests = ClassJoinRequest.objects.filter(class_requested=class_obj, status='pending').select_related('student')
        class_join_requests_map[class_obj] = join_requests
        print(f'Class {class_obj.subject_name} has {join_requests.count()} pending requests')
    
    has_pending = any(join_requests.exists() for join_requests in class_join_requests_map.values())
    print(f'Has pending requests: {has_pending}')

    # DEBUG: Print all pending join requests for this faculty's classes
    all_pending = ClassJoinRequest.objects.filter(class_requested__in=classes, status='pending')
    print(f'All pending join requests for faculty {faculty_id}: {list(all_pending)}')

    context = {
        'role': 'faculty',
        'faculty': faculty,
        'class_join_requests_map': dict(class_join_requests_map) ,
        'has_pending': has_pending,
    }
    return render(request, 'class_join_request/class_join_request_list.html', context)

def approve_join_request(request, request_id):
    join_request = get_object_or_404(ClassJoinRequest, id=request_id)
    join_request.status = 'approved'
    join_request.save()
    
    # Automatically enroll the student in the class
    Enrollment.objects.get_or_create(
        student=join_request.student,
        enrolled_class=join_request.class_requested,
        defaults={'date_enrolled': join_request.requested_at}
    )
    
    messages.success(request, f"Join request approved. {join_request.student.first_name} {join_request.student.last_name} has been enrolled in {join_request.class_requested.subject_name}.")
    return redirect(request.META.get('HTTP_REFERER', 'dashboard_faculty'))

def reject_join_request(request, request_id):
    join_request = get_object_or_404(ClassJoinRequest, id=request_id)
    join_request.status = 'rejected'
    join_request.save()
    messages.success(request, "Join request rejected.")
    return redirect(request.META.get('HTTP_REFERER', 'dashboard_faculty'))