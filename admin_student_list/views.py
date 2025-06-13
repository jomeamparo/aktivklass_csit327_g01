from django.shortcuts import redirect, render
from django.urls import reverse
from core.models import Student
from django.http import JsonResponse

def admin_student_list_view(request):
    if request.method == "POST":
        action = request.POST.get("action")
        student_id = request.POST.get("student_id")
        first_name = request.POST.get("first_name")
        middle_name = request.POST.get("middle_name", " ")
        last_name = request.POST.get("last_name")
        course = request.POST.get("course")
        year = request.POST.get("year")

        if action == "edit":
            try:
                student = Student.objects.get(student_id=student_id)
                student.first_name = first_name
                student.middle_name = middle_name if middle_name.strip() else " "
                student.last_name = last_name
                student.course = course
                student.year = year
                student.save()
                return JsonResponse({'success': True})
            except Student.DoesNotExist:
                return JsonResponse({'error': 'Student not found'}, status=404)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
        else:  # action == "add"
            if all([student_id, first_name, last_name, course, year]):
                if not Student.objects.filter(student_id=student_id).exists():
                    Student.objects.create(
                        student_id=student_id,
                        first_name=first_name,
                        middle_name=middle_name if middle_name.strip() else " ",
                        last_name=last_name,
                        course=course,
                        year=year,
                    )
                else:
                    return JsonResponse({'error': 'Student ID already exists'}, status=400)
            return redirect(reverse('student_list_view'))

    # For GET requests - list students
    students = Student.objects.all().order_by('student_id')
    context = {
        'students': students,
        'role': 'admin'
    }
    return render(request, 'admin_student_list/student_list.html', context)