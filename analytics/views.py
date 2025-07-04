from django.shortcuts import render
from django.http import JsonResponse
from core.models import Analytics, Faculty, Student


def analytics_view(request):
    # Update analytics stats
    analytics = Analytics.update_stats()
    
    context = {
        'total_faculty': analytics.total_faculty if analytics else Faculty.objects.count(),
        'total_students': analytics.total_students if analytics else Student.objects.count(),
        'role': request.session.get('role', '')
    }
    return render(request, 'analytics/analytics.html', context)


def get_faculty_count(request):
    count = Faculty.objects.count()
    return JsonResponse({'count': count})


def get_student_count(request):
    count = Student.objects.count()
    return JsonResponse({'count': count})
