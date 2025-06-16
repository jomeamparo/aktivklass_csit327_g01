from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
import csv
from core.models import Student

def admin_student_list_view(request):
    if request.method == "POST":
        # Handle file upload
        if 'class_list' in request.FILES:
            file = request.FILES['class_list']
            if file.name.endswith('.csv'):
                decoded_file = file.read().decode('utf-8').splitlines()
                reader = csv.DictReader(decoded_file)
                for row in reader:
                    if not Student.objects.filter(student_id=row['student_id']).exists():
                        Student.objects.create(
                            student_id=row['student_id'],
                            first_name=row['first_name'],
                            middle_name=row.get('middle_name', ' '),
                            last_name=row['last_name'],
                            course=row.get('course', ''),
                            year=row.get('year', '')
                        )
            return redirect(reverse('admin_student_list'))

        # Handle student creation/editing
        action = request.POST.get('action')
        student_id = request.POST.get('student_id')
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name', ' ')
        last_name = request.POST.get('last_name')
        course = request.POST.get('course')
        year = request.POST.get('year')

        if action == 'edit':
            try:
                student = Student.objects.get(student_id=student_id)
                student.first_name = first_name
                student.middle_name = middle_name if middle_name.strip() else ' '
                student.last_name = last_name
                student.course = course
                student.year = year
                student.save()
            except Student.DoesNotExist:
                pass
        else:
            if all([student_id, first_name, last_name, course, year]):
                if not Student.objects.filter(student_id=student_id).exists():
                    Student.objects.create(
                        student_id=student_id,
                        first_name=first_name,
                        middle_name=middle_name if middle_name.strip() else ' ',
                        last_name=last_name,
                        course=course,
                        year=year,
                    )

        return redirect(reverse('admin_student_list'))

    # For GET requests - list students
    students = Student.objects.all().order_by('last_name', 'first_name')
    context = {
        'students': students,
        'role': 'admin'
    }
    return render(request, 'admin_student_list/student_list.html', context)

@csrf_exempt
@require_POST
def toggle_student_status(request):
    try:
        data = json.loads(request.body)
        student_id = data.get('student_id')
        is_disabled = data.get('is_disabled')
        
        student = Student.objects.get(student_id=student_id)
        student.is_disabled = is_disabled
        student.save()
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)