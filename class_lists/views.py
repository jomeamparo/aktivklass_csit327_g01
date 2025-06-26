from django.shortcuts import render, get_object_or_404, redirect
from core.models import Class, Student, Enrollment, ClassJoinRequest, FavoriteClass
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
    pending_requests_count = 0
    if request.session.get('user_id'):
        try:
            student = Student.objects.get(student_id=request.session.get('user_id'))
            favorited_ids = list(FavoriteClass.objects.filter(student=student).values_list('class_obj_id', flat=True))
            pending_requests_count = ClassJoinRequest.objects.filter(student=student, status='pending').count()
        except Student.DoesNotExist:
            pass

    return render(request, 'class_lists/class_list.html', {
        'classes': classes,
        'role': role,
        'search_query': search_query,
        'favorited_ids': favorited_ids,
        'pending_requests_count': pending_requests_count,
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

# Feature 2: Pending Join Requests Indicator
def pending_requests_view(request):
    if not request.session.get('user_id'):
        messages.error(request, 'You must be logged in to view pending requests.')
        return redirect('class_list')
    
    try:
        student = Student.objects.get(student_id=request.session.get('user_id'))
        pending_requests = ClassJoinRequest.objects.filter(
            student=student,
            status='pending'
        ).select_related('class_requested')
        
        return render(request, 'class_lists/pending_requests.html', {
            'pending_requests': pending_requests,
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
        
        favorite, created = FavoriteClass.objects.get_or_create(
            student=student,
            class_obj=class_obj
        )
        
        if not created:
            # If it already exists, remove it (toggle off)
            favorite.delete()
            return JsonResponse({'favorited': False, 'message': 'Removed from favorites'})
        else:
            return JsonResponse({'favorited': True, 'message': 'Added to favorites'})
            
    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found.'}, status=404)
