from django.shortcuts import render

def student_settings(request):
    return render(request, 'student_settings/settings.html')
