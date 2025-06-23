from django.shortcuts import render
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from core.models import Faculty, PasswordResetToken, Student, AdminUser
from .token_generator import SimpleTokenGenerator

def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            found = False

            # Faculty
            try:
                faculty = Faculty.objects.get(email=email)
                token = SimpleTokenGenerator.generate_token()
                PasswordResetToken.objects.create(faculty=faculty, token=token)

                reset_link = f"http://127.0.0.1:8000/forgot_password/reset/{token}/"
                send_mail(
                    'Password Reset Request',
                    f'Click to reset your password:\n\n{reset_link}',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                found = True
            except Faculty.DoesNotExist:
                pass

            # Student
            try:
                student = Student.objects.get(email=email)
                token = SimpleTokenGenerator.generate_token()
                PasswordResetToken.objects.create(student=student, token=token)

                reset_link = f"http://127.0.0.1:8000/forgot_password/reset/{token}/"
                send_mail(
                    'Password Reset Request',
                    f'Click to reset your password:\n\n{reset_link}',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                found = True
            except Student.DoesNotExist:
                pass

                # Admin
            try:
                admin = AdminUser.objects.get(email=email)
                token = SimpleTokenGenerator.generate_token()
                PasswordResetToken.objects.create(admin_user=admin, token=token)

                reset_link = f"http://127.0.0.1:8000/forgot_password/reset/{token}/"
                send_mail(
                    'Password Reset Request',
                    f'Click to reset your password:\n\n{reset_link}',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                found = True
            except Student.DoesNotExist:
                pass
        
            messages.success(request, 'If an account with that email exists, a reset link has been sent.')
        else:
            messages.error(request, 'Please enter a valid email address.')

    return render(request, 'forgot_password/forgot_password_enterpass.html')


def reset_password_view(request, token):
    try:
        token_obj = PasswordResetToken.objects.get(token=token, is_used=False)
    except PasswordResetToken.DoesNotExist:
        messages.error(request, 'Invalid or expired reset link.')
        return render(request, 'forgot_password/forgot_password_reset.html', {'token': token})

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password and confirm_password:
            if new_password == confirm_password:
                if token_obj.faculty:
                    token_obj.faculty.password = new_password  # Replace with hashed version in production
                    token_obj.faculty.save()
                elif token_obj.student:
                    token_obj.student.password = new_password  # Replace with hashed version in production
                    token_obj.student.save()
                

                token_obj.is_used = True
                token_obj.save()

                messages.success(request, 'Your password has been reset successfully.')
            else:
                messages.error(request, 'Passwords do not match.')
        else:
            messages.error(request, 'Please fill in all fields.')

    return render(request, 'forgot_password/forgot_password_reset.html', {'token': token})
