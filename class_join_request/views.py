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

    # Get all enrollments for this faculty
    enrollments = Enrollment.objects.filter(faculty=faculty)

    # Get all related classes
    class_ids = enrollments.values_list('enrolled_class_id', flat=True)
    classes = Class.objects.filter(id__in=class_ids).order_by('subject_name')

    # Prepare a mapping of each class to its join requests
    class_join_requests_map = defaultdict(list)

    for class_obj in classes:
        join_requests = ClassJoinRequest.objects.filter(class_requested=class_obj, status='pending').select_related('student')
        class_join_requests_map[class_obj] = join_requests
    
    has_pending = any(join_requests.exists() for join_requests in class_join_requests_map.values())

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
    messages.success(request, "Join request approved.")
    return redirect(request.META.get('HTTP_REFERER', 'dashboard_faculty'))

def reject_join_request(request, request_id):
    join_request = get_object_or_404(ClassJoinRequest, id=request_id)
    join_request.status = 'rejected'
    join_request.save()
    messages.success(request, "Join request rejected.")
    return redirect(request.META.get('HTTP_REFERER', 'dashboard_faculty'))