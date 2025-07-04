from django.shortcuts import render, redirect
from django.http import JsonResponse
from core.models import Student  # Assuming your model is named student
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

def edit_student_view(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name', '')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        course = request.POST.get('course')
        year = request.POST.get('year')
        action = request.POST.get('action', '')

        if action == 'edit':
            # Edit existing student
            try:
                student = Student.objects.get(student_id=student_id)
                student.first_name = first_name
                student.middle_name = middle_name
                student.last_name = last_name
                student.course = course
                student.year = year
                student.save()
            except Student.DoesNotExist:
                pass  # Optional: handle not found
        else:
            # Add new Student (if not exists)
            Student.objects.update_or_create(
                student_id=student_id,
                defaults={
                    'first_name': first_name,
                    'middle_name': middle_name,
                    'last_name': last_name,
                    'email': email,
                    'course': course,
                    'year': year,
                    'status': 'ACTIVE'
                }
            )

        return redirect('edit_student')

    studentList = Student.objects.all()
    context = {
        'studentList': studentList,
        'role': 'admin'
    }
    return render(request, 'edit_student/edit_student.html', context)


@require_POST
def toggle_student_status(request, student_id):
    try:
        student = Student.objects.get(student_id=student_id)
        student.status = 'DISABLED' if student.status == 'ACTIVE' else 'ACTIVE'
        student.save()
        return JsonResponse({'success': True, 'status': student.status})
    except student.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Student not found'})
