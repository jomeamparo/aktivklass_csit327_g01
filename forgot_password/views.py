from django.shortcuts import render
from django.contrib import messages
from django.core.mail import send_mail  # optional for real email sending
from django.conf import settings


def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            # You would add logic here to check if user exists and send an actual reset link
            # For now, simulate success response
            messages.success(request, 'If an account with that email exists, a reset link has been sent.')

            # Uncomment below to send an actual email (you must configure EMAIL settings in settings.py)
            send_mail(
                'Reset Your Password',
                'Click the link to reset your password.',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

        else:
            messages.error(request, 'Please enter a valid email address.')
    return render(request, 'forgot_password/forgot_password_view.html')
