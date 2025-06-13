from django.shortcuts import redirect, render
from django.urls import reverse
from core.models import Faculty
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db import connection

def admin_faculty_list_view(request):
    if request.method == "POST":
        action = request.POST.get("action", "add")  # Default to add if not specified
        faculty_id = request.POST.get("faculty_id")
        first_name = request.POST.get("first_name")
        middle_name = request.POST.get("middle_name", " ")
        last_name = request.POST.get("last_name")
        college_name = request.POST.get("college_name")
        department_name = request.POST.get("department_name")

        if all([faculty_id, first_name, last_name, college_name, department_name]):
            if action == "edit":
                # Update existing faculty
                try:
                    faculty = Faculty.objects.get(faculty_id=faculty_id)
                    faculty.first_name = first_name
                    faculty.middle_name = middle_name if middle_name.strip() else " "
                    faculty.last_name = last_name
                    faculty.college_name = college_name
                    faculty.department_name = department_name
                    faculty.save()
                except Faculty.DoesNotExist:
                    pass  # Handle error if needed
            else:
                # Add new faculty
                if not Faculty.objects.filter(faculty_id=faculty_id).exists():
                    Faculty.objects.create(
                        faculty_id=faculty_id,
                        first_name=first_name,
                        middle_name=middle_name if middle_name.strip() else " ",
                        last_name=last_name,
                        college_name=college_name,
                        department_name=department_name,
                    )

        return redirect(reverse('admin_faculty_list'))

    facultyList = Faculty.objects.all().order_by('faculty_id')
    context = {
        'facultyList': facultyList,
        'role': 'admin'
    }
    return render(request, 'admin_faculty_list/faculty_list.html', context)

@require_POST
def toggle_faculty_status(request, faculty_id):
    try:
        faculty = Faculty.objects.get(faculty_id=faculty_id)
        faculty.status = 'DISABLED' if faculty.status == 'ACTIVE' else 'ACTIVE'
        faculty.save()
        return JsonResponse({
            'success': True,
            'status': faculty.status,
            'message': f"Faculty account {'disabled' if faculty.status == 'DISABLED' else 'activated'} successfully!"
        })
    except Faculty.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Faculty not found.'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })