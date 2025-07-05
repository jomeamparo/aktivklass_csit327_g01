from django.shortcuts import render
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password
from core.models import Faculty, Student, AdminUser, PasswordResetToken
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
                try:
                    send_mail(
                        'Password Reset Request',
                        f'Click to reset your password:\n\n{reset_link}',
                        settings.DEFAULT_FROM_EMAIL,
                        [email],
                        fail_silently=False,
                    )
                except Exception as e:
                    print("Error sending email to faculty:", e)

                found = True
            except Faculty.DoesNotExist:
                pass

            # Student
            try:
                student = Student.objects.get(email=email)
                token = SimpleTokenGenerator.generate_token()
                PasswordResetToken.objects.create(student=student, token=token)

                reset_link = f"http://127.0.0.1:8000/forgot_password/reset/{token}/"
                try:
                    send_mail(
                        'Password Reset Request',
                        f'Click to reset your password:\n\n{reset_link}',
                        settings.DEFAULT_FROM_EMAIL,
                        [email],
                        fail_silently=False,
                    )
                except Exception as e:
                    print("Error sending email to student:", e)

                found = True
            except Student.DoesNotExist:
                pass

            # Admin
            try:
                admin = AdminUser.objects.get(email=email)
                token = SimpleTokenGenerator.generate_token()
                PasswordResetToken.objects.create(admin_user=admin, token=token)

                reset_link = f"http://127.0.0.1:8000/forgot_password/reset/{token}/"
                try:
                    send_mail(
                        'Password Reset Request',
                        f'Click to reset your password:\n\n{reset_link}',
                        settings.DEFAULT_FROM_EMAIL,
                        [email],
                        fail_silently=False,
                    )
                except Exception as e:
                    print("Error sending email to admin:", e)

                found = True
            except AdminUser.DoesNotExist:
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
                    token_obj.faculty.password = new_password
                    token_obj.faculty.save()
                elif token_obj.student:
                    token_obj.student.password = new_password
                    token_obj.student.save()
                elif token_obj.admin_user:
                    token_obj.admin_user.password = new_password
                    token_obj.admin_user.save()

                token_obj.is_used = True
                token_obj.save()

                messages.success(request, 'Your password has been reset successfully.')
            else:
                messages.error(request, 'Passwords do not match.')
        else:
            messages.error(request, 'Please fill in all fields.')

    return render(request, 'forgot_password/forgot_password_reset.html', {'token': token})

def test_email_view(request):
    result = None
    if request.method == 'POST':
        to_email = request.POST.get('email')
        try:
            send_mail(
                'Test Email',
                'This is a test email from your Django app.',
                settings.DEFAULT_FROM_EMAIL,
                [to_email],
                fail_silently=False,
            )
            result = f"Test email sent to {to_email}. Check your inbox and spam folder."
        except Exception as e:
            result = f"Error sending test email: {e}"
    return render(request, 'forgot_password/test_email.html', {'result': result})
