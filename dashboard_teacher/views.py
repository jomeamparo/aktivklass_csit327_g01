from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from core.models import Class, Faculty
from django.contrib import messages

# @login_required
def dashboard_view(request):
    classes = Class.objects.filter(is_archived=False)
    return render(request, 'dashboard_teacher/dashboard.html', {'classes': classes, 'role': 'faculty'})

@require_POST
@csrf_exempt  # Remove this if you're using CSRF token correctly in the form
def create_class(request):
    subject_name = request.POST.get('subject_name')
    subject_code = request.POST.get('subject_code')
    description = request.POST.get('description')
    schedule = request.POST.get('schedule')
    room = request.POST.get('room')
    
    # Get the faculty who is creating the class
    faculty_id = request.session.get('user_id')
    faculty = None
    
    if faculty_id:
        try:
            faculty = Faculty.objects.get(faculty_id=faculty_id)
        except Faculty.DoesNotExist:
            pass

    new_class = Class.objects.create(
        subject_name=subject_name,
        subject_code=subject_code,
        description=description,
        schedule=schedule,
        room=room,
        faculty=faculty  # Assign the faculty who created the class
    )

    return JsonResponse({
        'id': new_class.id,
        'class_code': new_class.class_code,
        'subject_name': new_class.subject_name,
        'subject_code': new_class.subject_code,
        'description': new_class.description,
        'schedule': new_class.schedule,
        'room': new_class.room,
        'faculty_assigned': faculty.first_name + " " + faculty.last_name if faculty else "No faculty assigned"
    })

def delete_class(request, class_id):
    if request.method == "POST":
        class_instance = get_object_or_404(Class, id=class_id)
        class_instance.delete()
        return redirect('dashboard_teacher')
    return redirect('dashboard_teacher')

def archive_class(request, class_id):
    if request.method == "POST":
        class_instance = get_object_or_404(Class, id=class_id)
        class_instance.is_archived = True  # Make sure this field exists in your model
        class_instance.save()
        return redirect('dashboard_teacher')
    return redirect('dashboard_teacher')

