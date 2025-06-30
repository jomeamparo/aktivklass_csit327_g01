from django.shortcuts import render, redirect
from django.http import JsonResponse
from core.models import Faculty  # Assuming your model is named Faculty
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

def edit_faculty_view(request):
    if request.method == 'POST':
        faculty_id = request.POST.get('faculty_id')
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name', '')
        last_name = request.POST.get('last_name')
        college_name = request.POST.get('college_name')
        department_name = request.POST.get('department_name')
        action = request.POST.get('action', '')

        if action == 'edit':
            # Edit existing faculty
            try:
                faculty = Faculty.objects.get(faculty_id=faculty_id)
                faculty.first_name = first_name
                faculty.middle_name = middle_name
                faculty.last_name = last_name
                faculty.college_name = college_name
                faculty.department_name = department_name
                faculty.save()
            except Faculty.DoesNotExist:
                pass  # Optional: handle not found
        else:
            # Add new faculty (if not exists)
            Faculty.objects.update_or_create(
                faculty_id=faculty_id,
                defaults={
                    'first_name': first_name,
                    'middle_name': middle_name,
                    'last_name': last_name,
                    'college_name': college_name,
                    'department_name': department_name,
                    'status': 'ACTIVE'
                }
            )

        return redirect('edit_faculty')

    facultyList = Faculty.objects.all()
    context = {
        'facultyList': facultyList,
        'role': 'admin'
    }
    return render(request, 'edit_faculty/edit_faculty.html', context)


@require_POST
def toggle_faculty_status(request, faculty_id):
    try:
        faculty = Faculty.objects.get(faculty_id=faculty_id)
        faculty.status = 'DISABLED' if faculty.status == 'ACTIVE' else 'ACTIVE'
        faculty.save()
        return JsonResponse({'success': True, 'status': faculty.status})
    except Faculty.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Faculty not found'})
