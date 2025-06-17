from django.shortcuts import render
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from core.models import Faculty, PasswordResetToken
from .token_generator import SimpleTokenGenerator

def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            try:
                faculty = Faculty.objects.get(email=email)
                # Generate and save a token in the DB
                token = SimpleTokenGenerator.generate_token()
                PasswordResetToken.objects.create(faculty=faculty, token=token)
                reset_link = f"http://127.0.0.1:8000/forgot_password/reset/{token}/"
                send_mail(
                    'Password Reset Request',
                    f'This is an email to reset your password.\nClick the link below to reset your password:\n\n{reset_link}',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                messages.success(request, 'If an account with that email exists, a reset link has been sent.')
            except Faculty.DoesNotExist:
                messages.success(request, 'If an account with that email exists, a reset link has been sent.')
        else:
            messages.error(request, 'Please enter a valid email address.')
    # Render the forgot password form (not the reset form)
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
                faculty = token_obj.faculty
                faculty.password = new_password  # Hash in production!
                faculty.save()
                token_obj.is_used = True
                token_obj.save()
                messages.success(request, 'Your password has been reset successfully.')
            else:
                messages.error(request, 'Passwords do not match.')
        else:
            messages.error(request, 'Please fill in all fields.')

    return render(request, 'forgot_password/forgot_password_reset.html', {'token': token})
