from django.shortcuts import redirect, render
from django.urls import reverse

from core.models import Faculty

def dashboard_view(request):
    if request.method == "POST":
        faculty_id = request.POST.get("faculty_id")
        first_name = request.POST.get("first_name")
        middle_name = request.POST.get("middle_name", " ")
        last_name = request.POST.get("last_name")
        college_name = request.POST.get("college_name")
        department_name = request.POST.get("department_name")

        if all([faculty_id, first_name, last_name, college_name, department_name]):
            if not Faculty.objects.filter(faculty_id=faculty_id).exists():
                Faculty.objects.create(
                    faculty_id=faculty_id,
                    first_name=first_name,
                    middle_name=middle_name if middle_name.strip() else " ",
                    last_name=last_name,
                    college_name=college_name,
                    department_name=department_name,
                )
            else:
                pass

        return redirect(reverse('admin_faculty_list'))

    facultyList = Faculty.objects.all().order_by('faculty_id')
    context = {
        'facultyList': facultyList,
        'role': 'admin'
    }
    return render(request, 'dashboard_admin/dashboard.html', context)