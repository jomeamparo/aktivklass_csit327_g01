<<<<<<< HEAD
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from core.models import Faculty

def edit_faculty_view(request):
    facultyList = Faculty.objects.all()
    return render(request, 'edit_faculty/edit_faculty.html', {'facultyList': facultyList})
=======
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from core.models import Faculty
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)

def faculty_list_view(request):
    faculties = Faculty.objects.all()
    return render(request, 'edit_faculty/faculty_list.html', {'faculties': faculties})

@require_POST
def update_faculty(request, faculty_id):
    logger.info(f"Updating faculty {faculty_id}. POST data: {request.POST}")
    try:
        faculty = get_object_or_404(Faculty, faculty_id=faculty_id)
        
        faculty.first_name = request.POST.get('first_name')
        faculty.middle_name = request.POST.get('middle_name')
        faculty.last_name = request.POST.get('last_name')
        faculty.college_name = request.POST.get('college_name')
        faculty.department_name = request.POST.get('department_name')
        faculty.email = request.POST.get('email')
        faculty.status = request.POST.get('status')
        
        faculty.full_clean()
        faculty.save()

        # If faculty is linked to a user, update user details
        try:
            user = User.objects.get(email=faculty.email)
            user.first_name = faculty.first_name
            user.last_name = faculty.last_name
            user.save()
        except User.DoesNotExist:
            # Handle case where no user is associated (optional)
            pass

        return JsonResponse({'success': True, 'message': 'Faculty information updated successfully.'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)

def edit_faculty_view(request, faculty_id):
    faculty = get_object_or_404(Faculty, faculty_id=faculty_id)
    status_choices = Faculty._meta.get_field('status').choices
    
    context = {
        'faculty': faculty,
        'status_choices': status_choices,
    }
    return render(request, 'edit_faculty/edit_faculty.html', context)
>>>>>>> 77c7325 (feature/edit_student/setup_3)
