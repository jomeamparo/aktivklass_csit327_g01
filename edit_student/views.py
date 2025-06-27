from django.shortcuts import render
from core.models import Student

def edit_student_view(request):
    students = Student.objects.all()
    return render(request, 'edit_student/edit_student.html', {'students': students})
