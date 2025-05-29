from django.shortcuts import render, redirect
from django.urls import reverse
from core.models import Student, Class

def teacher_student_list_view(request):
    if request.method == "POST":
        student_id = request.POST.get("student_id")
        first_name = request.POST.get("first_name")
        middle_name = request.POST.get("middle_name", " ")
        last_name = request.POST.get("last_name")
        course = request.POST.get("course")
        year = request.POST.get("year")

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
        return redirect(reverse('teacher_student_list'))

    # Get all classes that have enrolled students
    classes = Class.objects.prefetch_related('students').all()

    class_students = []
    for c in classes:
        students_in_class = c.students.all().order_by('last_name', 'first_name')

        if students_in_class.exists():  # Only include if there are students
            class_students.append({
                'class_id': c.id,
                'subject_code': c.subject_code,
                'subject_name': c.subject_name,
                'students': [{
                    'first_name': s.first_name,
                    'middle_name': s.middle_name,
                    'last_name': s.last_name,
                    'course': s.course,
                    'year': s.year
                } for s in students_in_class]
            })

    context = {
        'class_students': class_students,
        'role': 'faculty',
    }
    return render(request, 'teacher_student/teacher_student_list.html', context)
