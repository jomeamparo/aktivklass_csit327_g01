from django.shortcuts import render, get_object_or_404, redirect
from core.models import Class, Student, Enrollment, ClassJoinRequest, FavoriteCourse, Course
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse

def class_list_view(request):
    classes = Class.objects.filter(is_archived=False)
    
    # Feature 1: Search and Filter
    search_query = request.GET.get('q', '')
    if search_query:
        classes = classes.filter(
            Q(subject_name__icontains=search_query) |
            Q(subject_code__icontains=search_query)
        )

    role = request.session.get('role')  # or use however you normally store it
    
    # Feature 3: Bookmark / Favorite Class
    favorited_ids = []
    requests_sent_count = 0
    if request.session.get('user_id'):
        try:
            student = Student.objects.get(student_id=request.session.get('user_id'))
            # Get the course IDs that are favorited by this student
            favorited_course_ids = list(FavoriteCourse.objects.filter(student=student).values_list('course_id', flat=True))
            # Get class IDs that are linked to the favorited courses
            favorited_ids = list(Class.objects.filter(course_id__in=favorited_course_ids).values_list('id', flat=True))
            requests_sent_count = ClassJoinRequest.objects.filter(student=student).count()
        except Student.DoesNotExist:
            pass

    return render(request, 'class_lists/class_list.html', {
        'classes': classes,
        'role': role,
        'search_query': search_query,
        'favorited_ids': favorited_ids,
        'pending_requests_count': requests_sent_count,
    })

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
        
        # Check if there's already any request (pending, approved, or rejected)
        existing_request = ClassJoinRequest.objects.filter(
            student=student,
            class_requested=selected_class
        ).first()

        if existing_request:
            if existing_request.status == 'pending':
                messages.warning(request, 'You already have a pending request to join this class.')
            elif existing_request.status == 'approved':
                messages.info(request, 'Your request to join this class has already been approved.')
            elif existing_request.status == 'rejected':
                messages.warning(request, 'Your previous request to join this class was rejected.')
            else:
                messages.warning(request, 'You have already requested to join this class.')
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

# Feature 2: Requests Sent Indicator
def pending_requests_view(request):
    if not request.session.get('user_id'):
        messages.error(request, 'You must be logged in to view your requests.')
        return redirect('class_list')
    
    try:
        student = Student.objects.get(student_id=request.session.get('user_id'))
        all_requests = ClassJoinRequest.objects.filter(
            student=student
        ).select_related('class_requested').order_by('-requested_at')
        
        return render(request, 'class_lists/pending_requests.html', {
            'pending_requests': all_requests,
        })
    except Student.DoesNotExist:
        messages.error(request, 'Student not found.')
        return redirect('class_list')

# Feature 3: Bookmark / Favorite Class
def toggle_favorite_view(request, class_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    if not request.session.get('user_id'):
        return JsonResponse({'error': 'You must be logged in to favorite classes.'}, status=401)
    
    try:
        student = Student.objects.get(student_id=request.session.get('user_id'))
        class_obj = get_object_or_404(Class, id=class_id)
        
        # Use the direct relationship between Class and Course
        if not class_obj.course:
            return JsonResponse({'error': 'This class is not linked to a course.'}, status=404)
        
        favorite, created = FavoriteCourse.objects.get_or_create(
            student=student,
            course=class_obj.course
        )
        
        if not created:
            # If it already exists, remove it (toggle off)
            favorite.delete()
            return JsonResponse({'favorited': False, 'message': 'Removed from favorites'})
        else:
            return JsonResponse({'favorited': True, 'message': 'Added to favorites'})
            
    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found.'}, status=404)
