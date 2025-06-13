from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def student_settings(request):
    return render(request, 'student_settings/settings.html')
