from django.shortcuts import render, redirect

from core.models import AdminUser, Faculty, Student
from .forms import LoginForm
from django.contrib import messages

def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user_id = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            try:
                faculty = Faculty.objects.get(faculty_id=user_id, password=password)
                request.session['user_id'] = faculty.faculty_id
                messages.success(request, "Login successful!")
                return redirect('dashboard_teacher')  # faculty dashboard
            except Faculty.DoesNotExist:
                pass

            try:
                admin_user = AdminUser.objects.get(employee_id=user_id, password=password)
                request.session['user_id'] = admin_user.employee_id
                messages.success(request, "Login successful!")
                return redirect('dashboard_admin')  # admin dashboard
            except AdminUser.DoesNotExist:
                pass

            try:
                student = Student.objects.get(student_id=user_id, password=password)
                request.session['user_id'] = student.student_id
                messages.success(request, "Login successful!")
                return redirect('dashboard_student')  # student dashboard
            except Student.DoesNotExist:
                pass

            messages.error(request, "Invalid user ID or password.")

    return render(request, 'login/login.html', {'form': form})

