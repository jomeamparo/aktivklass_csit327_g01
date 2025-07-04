from django.shortcuts import render
from django.http import JsonResponse
from core.models import Analytics, Faculty, Student
from django.db.models import Count


def analytics_view(request):
    # Update analytics stats
    analytics = Analytics.update_stats()
    
    # Name College
    colleges = Faculty.objects.values_list('college_name', flat=True).distinct().order_by('college_name')
    
    # Student Course
    courses = Student.objects.values_list('course', flat=True).distinct().order_by('course').exclude(course__isnull=True).exclude(course='')
    
    # GStudent year
    years = Student.objects.values_list('year', flat=True).distinct().order_by('year').exclude(year__isnull=True).exclude(year='')
    
    context = {
        'total_faculty': analytics.total_faculty if analytics else Faculty.objects.count(),
        'total_students': analytics.total_students if analytics else Student.objects.count(),
        'active_faculty': Faculty.objects.filter(status='ACTIVE').count(),
        'colleges': colleges,
        'courses': courses,
        'years': years,
        'role': request.session.get('role', '')
    }
    return render(request, 'analytics/analytics.html', context)


def get_faculty_count(request):
    count = Faculty.objects.count()
    return JsonResponse({'count': count})


def get_student_count(request):
    count = Student.objects.count()
    return JsonResponse({'count': count})


def get_active_faculty_count(request):
    count = Faculty.objects.filter(status='ACTIVE').count()
    return JsonResponse({'count': count})


def get_faculty_by_status(request):
    status = request.GET.get('status')
    if status:
        count = Faculty.objects.filter(status=status).count()
        return JsonResponse({'count': count})
    return JsonResponse({'count': 0})


def get_faculty_by_college(request):
    college_name = request.GET.get('college_id')
    if college_name:
        count = Faculty.objects.filter(college_name=college_name).count()
        return JsonResponse({'count': count})
    return JsonResponse({'count': 0})


def get_colleges(request):
    colleges = list(Faculty.objects.values_list('college_name', flat=True).distinct().order_by('college_name'))
    return JsonResponse({'colleges': colleges})


def get_students_by_course(request):
    course = request.GET.get('course_id')
    if course:
        count = Student.objects.filter(course=course).count()
        return JsonResponse({'count': count})
    return JsonResponse({'count': 0})


def get_students_by_year(request):
    year = request.GET.get('year_id')
    if year:
        count = Student.objects.filter(year=year).count()
        return JsonResponse({'count': count})
    return JsonResponse({'count': 0})


def get_courses(request):
    courses = list(Student.objects.values_list('course', flat=True).distinct().order_by('course').exclude(course__isnull=True).exclude(course=''))
    return JsonResponse({'courses': courses})


def get_years(request):
    years = list(Student.objects.values_list('year', flat=True).distinct().order_by('year').exclude(year__isnull=True).exclude(year=''))
    return JsonResponse({'years': years})


def get_account_status_chart_data(request):
    """Get data for account status pie chart"""
    active_count = Faculty.objects.filter(status='ACTIVE').count()
    disabled_count = Faculty.objects.filter(status='DISABLED').count()
    
    data = {
        'labels': ['Active', 'Disabled'],
        'data': [active_count, disabled_count],
        'colors': ['#10B981', '#059669']  # Green shades
    }
    return JsonResponse(data)


def get_faculty_college_chart_data(request):
    """Get data for faculty by college pie chart"""
    colleges_data = Faculty.objects.values('college_name').annotate(count=Count('college_name')).order_by('college_name')
    
    labels = []
    data = []
    
    for college in colleges_data:
        labels.append(college['college_name'])
        data.append(college['count'])
    
    # Generate green shades for each college
    colors = ['#10B981', '#059669', '#047857', '#065F46', '#064E3B', '#022C22']
    # If we have more colleges than colors, cycle through the colors
    while len(colors) < len(labels):
        colors.extend(['#10B981', '#059669', '#047857', '#065F46', '#064E3B', '#022C22'])
    colors = colors[:len(labels)]
    
    chart_data = {
        'labels': labels,
        'data': data,
        'colors': colors
    }
    return JsonResponse(chart_data)


def get_student_course_chart_data(request):
    """Get data for student by course pie chart"""
    courses_data = Student.objects.values('course').annotate(count=Count('course')).exclude(course__isnull=True).exclude(course='').order_by('course')
    
    labels = []
    data = []
    
    for course in courses_data:
        labels.append(course['course'])
        data.append(course['count'])
    
    # Generate green shades for each course
    colors = ['#10B981', '#059669', '#047857', '#065F46', '#064E3B', '#022C22']
    # If we have more courses than colors, cycle through the colors
    while len(colors) < len(labels):
        colors.extend(['#10B981', '#059669', '#047857', '#065F46', '#064E3B', '#022C22'])
    colors = colors[:len(labels)]
    
    chart_data = {
        'labels': labels,
        'data': data,
        'colors': colors
    }
    return JsonResponse(chart_data)


def get_student_year_chart_data(request):
    """Get data for student by year pie chart"""
    years_data = Student.objects.values('year').annotate(count=Count('year')).exclude(year__isnull=True).exclude(year='').order_by('year')
    
    labels = []
    data = []
    
    for year in years_data:
        labels.append(f"Year {year['year']}")
        data.append(year['count'])
    
    # Generate green shades for each year
    colors = ['#10B981', '#059669', '#047857', '#065F46', '#064E3B', '#022C22']
    # If we have more years than colors, cycle through the colors
    while len(colors) < len(labels):
        colors.extend(['#10B981', '#059669', '#047857', '#065F46', '#064E3B', '#022C22'])
    colors = colors[:len(labels)]
    
    chart_data = {
        'labels': labels,
        'data': data,
        'colors': colors
    }
    return JsonResponse(chart_data)
