from django.shortcuts import redirect, render
from django.urls import reverse
from core.models import Student

def admin_student_list_view(request):
    if request.method == "POST":
        student_id = request.POST.get("student_id")
        first_name = request.POST.get("first_name")
        middle_name = request.POST.get("middle_name", " ")
        last_name = request.POST.get("last_name")
        course = request.POST.get("course")
        year = request.POST.get("year")

        if all([student_id, first_name, last_name, course, year]):
            # Prevent duplicate student_id (optional)
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
                # Optionally, handle duplicate student_id error here (e.g. message)
                pass

        # Redirect to the same page to avoid resubmission on refresh
        return redirect(reverse('teacher_student_list'))

    # For GET requests - list students
    students = Student.objects.all().order_by('student_id')
    context = {
        'students': students,
        'role': 'admin'
    }
    return render(request, 'admin_student_list/student_list.html', context)