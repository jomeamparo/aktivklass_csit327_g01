from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from collections import defaultdict
import logging
from django.http import JsonResponse

from core.models import Class, ClassJoinRequest, Enrollment, Faculty

# Set up logging
logger = logging.getLogger(__name__)

def debug_join_requests(request):
    """Debug view to check join requests status"""
    logger.info("Debug join requests view accessed")
    
    # Get all join requests
    all_requests = ClassJoinRequest.objects.all().select_related('student', 'class_requested', 'class_requested__faculty')
    
    # Get faculty_id from session
    faculty_id = request.session.get('user_id')
    
    debug_info = {
        'faculty_id_in_session': faculty_id,
        'total_requests': all_requests.count(),
        'pending_requests': all_requests.filter(status='pending').count(),
        'all_requests': list(all_requests),
        'faculty_classes': [],
        'faculty_pending_requests': []
    }
    
    if faculty_id:
        try:
            faculty = Faculty.objects.get(faculty_id=faculty_id)
            debug_info['faculty_found'] = True
            debug_info['faculty_name'] = f"{faculty.first_name} {faculty.last_name}"
            
            # Get classes taught by this faculty
            faculty_classes = Class.objects.filter(faculty=faculty)
            debug_info['faculty_classes'] = list(faculty_classes)
            
            # Get pending requests for faculty's classes
            faculty_pending = ClassJoinRequest.objects.filter(
                class_requested__in=faculty_classes,
                status='pending'
            ).select_related('student', 'class_requested')
            debug_info['faculty_pending_requests'] = list(faculty_pending)
            
        except Faculty.DoesNotExist:
            debug_info['faculty_found'] = False
            debug_info['error'] = f"Faculty with ID {faculty_id} not found"
    
    return JsonResponse(debug_info)

def class_join_request_view(request):
    logger.info("Class join request view accessed")
    
    # Get faculty_id from session
    faculty_id = request.session.get('user_id')
    logger.info(f"Faculty ID from session: {faculty_id}")
    
    print('faculty_id:: ', faculty_id)
    if not faculty_id:
        logger.error("No faculty_id in session")
        messages.error(request, 'Faculty authentication required')
        return redirect('login')  # or your login route

    try:
        faculty = Faculty.objects.get(faculty_id=faculty_id)
        logger.info(f"Found faculty: {faculty}")
    except Faculty.DoesNotExist:
        logger.error(f"Faculty with ID {faculty_id} not found")
        messages.error(request, 'Faculty not found')
        return redirect('login')

    # Get all classes taught by this faculty
    classes = Class.objects.filter(faculty=faculty).order_by('subject_name')
    logger.info(f"Faculty {faculty.first_name} teaches {classes.count()} classes")
    print(f'Faculty {faculty.first_name} teaches {classes.count()} classes: {[c.subject_name for c in classes]}')

    # Prepare a mapping of each class to its join requests
    class_join_requests_map = defaultdict(list)

    for class_obj in classes:
        join_requests = ClassJoinRequest.objects.filter(class_requested=class_obj, status='pending').select_related('student')
        class_join_requests_map[class_obj] = join_requests
        logger.info(f"Class {class_obj.subject_name} has {join_requests.count()} pending requests")
        print(f'Class {class_obj.subject_name} has {join_requests.count()} pending requests')
    
    has_pending = any(join_requests.exists() for join_requests in class_join_requests_map.values())
    logger.info(f"Has pending requests: {has_pending}")
    print(f'Has pending requests: {has_pending}')

    # DEBUG: Print all pending join requests for this faculty's classes
    all_pending = ClassJoinRequest.objects.filter(class_requested__in=classes, status='pending')
    logger.info(f"All pending join requests for faculty {faculty_id}: {list(all_pending)}")
    print(f'All pending join requests for faculty {faculty_id}: {list(all_pending)}')

    context = {
        'role': 'faculty',
        'faculty': faculty,
        'class_join_requests_map': dict(class_join_requests_map) ,
        'has_pending': has_pending,
        'debug_info': {
            'faculty_id': faculty_id,
            'classes_count': classes.count(),
            'pending_requests_count': all_pending.count(),
            'all_pending_requests': list(all_pending)
        }
    }
    return render(request, 'class_join_request/class_join_request_list.html', context)

def approve_join_request(request, request_id):
    logger.info(f"Approving join request {request_id}")
    
    try:
        join_request = get_object_or_404(ClassJoinRequest, id=request_id)
        logger.info(f"Found join request: {join_request}")
        
        join_request.status = 'approved'
        join_request.save()
        logger.info(f"Join request {request_id} approved")
        
        # Automatically enroll the student in the class
        enrollment, created = Enrollment.objects.get_or_create(
            student=join_request.student,
            enrolled_class=join_request.class_requested,
            defaults={'date_enrolled': join_request.requested_at}
        )
        
        if created:
            logger.info(f"Created enrollment for student {join_request.student} in class {join_request.class_requested}")
        else:
            logger.info(f"Enrollment already exists for student {join_request.student} in class {join_request.class_requested}")
        
        messages.success(request, f"Join request approved. {join_request.student.first_name} {join_request.student.last_name} has been enrolled in {join_request.class_requested.subject_name}.")
        return redirect(request.META.get('HTTP_REFERER', 'dashboard_faculty'))
        
    except Exception as e:
        logger.error(f"Error approving join request {request_id}: {e}")
        messages.error(request, f"Error approving join request: {e}")
        return redirect(request.META.get('HTTP_REFERER', 'dashboard_faculty'))

def reject_join_request(request, request_id):
    logger.info(f"Rejecting join request {request_id}")
    
    try:
        join_request = get_object_or_404(ClassJoinRequest, id=request_id)
        logger.info(f"Found join request: {join_request}")
        
        join_request.status = 'rejected'
        join_request.save()
        logger.info(f"Join request {request_id} rejected")
        
        messages.success(request, "Join request rejected.")
        return redirect(request.META.get('HTTP_REFERER', 'dashboard_faculty'))
        
    except Exception as e:
        logger.error(f"Error rejecting join request {request_id}: {e}")
        messages.error(request, f"Error rejecting join request: {e}")
        return redirect(request.META.get('HTTP_REFERER', 'dashboard_faculty'))