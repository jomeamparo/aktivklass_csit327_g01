from django.shortcuts import render

def student_settings(request):
    context = {
        'role': 'student'
    }
    return render(request, 'student_settings/settings.html', context)
