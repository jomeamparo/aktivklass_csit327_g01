from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse
from core.models import Student
from django.views.decorators.http import require_POST

@require_POST
def toggle_student_status(request, student_id):
    try:
        student = Student.objects.get(student_id=student_id)
        student.status = 'DISABLED' if student.status == 'ACTIVE' else 'ACTIVE'
        student.save()
        return JsonResponse({
            'success': True,
            'status': student.status,
            'message': f"Student account {'disabled' if student.status == 'DISABLED' else 'activated'} successfully!"
        })
    except Student.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Student not found.'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })

def admin_student_list_view(request):
    if request.method == "POST":
        action = request.POST.get("action", "add")  # Default to add if not specified
        student_id = request.POST.get("student_id")
        first_name = request.POST.get("first_name")
        middle_name = request.POST.get("middle_name", " ")
        last_name = request.POST.get("last_name")
        course = request.POST.get("course")
        year = request.POST.get("year")

        if all([student_id, first_name, last_name, course, year]):
            try:
                if action == "edit":
                    # Update existing student
                    student = Student.objects.get(student_id=student_id)
                    student.first_name = first_name
                    student.middle_name = middle_name if middle_name.strip() else " "
                    student.last_name = last_name
                    student.course = course
                    student.year = year
                    student.save()
                    messages.success(request, f"Student {student_id} updated successfully!")
                else:
                    # Add new student
                    if not Student.objects.filter(student_id=student_id).exists():
                        Student.objects.create(
                            student_id=student_id,
                            first_name=first_name,
                            middle_name=middle_name if middle_name.strip() else " ",
                            last_name=last_name,
                            course=course,
                            year=year,
                        )
                        messages.success(request, f"Student {student_id} added successfully!")
                    else:
                        messages.error(request, f"Student ID {student_id} already exists!")
            except Student.DoesNotExist:
                messages.error(request, f"Student {student_id} not found!")
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
        else:
            messages.error(request, "Please fill in all required fields!")

        return redirect(reverse('student_list_view'))

    # For GET requests - list students
    students = Student.objects.all().order_by('student_id')
    context = {
        'students': students,
        'role': 'admin'
    }
    return render(request, 'admin_student_list/student_list.html', context)