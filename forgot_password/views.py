from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

# forgot_password/views.py
def forgot_password_view(request):  # ✅ matches your import
    return render(request, 'forgot_password/forgot_password_view.html')
