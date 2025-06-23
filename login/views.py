from django.shortcuts import render, redirect
from core.models import AdminUser, Faculty, Student
from .forms import LoginForm
from django.contrib import messages

def login_view(request):
    form = LoginForm(request.POST or None)
    
    # Get 'next' parameter from either GET or POST
    next_url = request.GET.get('next') or request.POST.get('next')
    
    if request.method == 'POST':
        if form.is_valid():
            user_id = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            try:
                faculty = Faculty.objects.get(faculty_id=user_id, password=password)
                request.session['user_id'] = faculty.faculty_id
                messages.success(request, "Login successful!")
                
                # Redirect to 'next' URL if provided, otherwise to dashboard
                if next_url:
                    return redirect(next_url)
                return redirect('dashboard_teacher')
            except Faculty.DoesNotExist:
                pass

            try:
                admin_user = AdminUser.objects.get(employee_id=user_id, password=password)
                request.session['user_id'] = admin_user.employee_id
                messages.success(request, "Login successful!")
                
                # Redirect to 'next' URL if provided, otherwise to dashboard
                if next_url:
                    return redirect(next_url)
                return redirect('dashboard_admin')
            except AdminUser.DoesNotExist:
                pass

            try:
                student = Student.objects.get(student_id=user_id, password=password)
                request.session['user_id'] = student.student_id
                messages.success(request, "Login successful!")
                
                # Redirect to 'next' URL if provided, otherwise to dashboard
                if next_url:
                    return redirect(next_url)
                return redirect('dashboard_student')
            except Student.DoesNotExist:
                pass

            messages.error(request, "Invalid user ID or password.")

    return render(request, 'login/login.html', {'form': form, 'next': next_url})


def forgot_password(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'login/forgot_password.html')

        updated = False
        for Model in (Faculty, AdminUser, Student):
            try:
                user = Model.objects.get(pk=user_id)
                user.password = new_password
                user.save()
                updated = True
                break
            except Model.DoesNotExist:
                continue

        if updated:
            messages.success(request, "Password updated successfully. Please login.")
            return redirect('login')
        else:
            messages.error(request, "User not found.")
            return render(request, 'login/forgot_password.html')

    return render(request, 'login/forgot_password.html')
