from django.shortcuts import render
from core.models import Class

def laboratory_view(request):
    class_data = {
        'subject_name': 'Information Management 2',
        'subject_code': 'CSIT327',
        'description': 'Basic principles and practices of collecting, organizing, storing, and using information effectively within organizations.',
        'schedule': 'MWF 12:00PM - 3:00PM',
        'room': 'Room NGE102',
        'class_code': 'M101A'
    }
    activities = ['Quiz 1', 'Quiz 2', 'Project', 'Exam']
    students = [
        {'name': 'Alice Santos', 'scores': [90, 85, 92, 88]},
        {'name': 'Bob Dela Cruz', 'scores': [78, 80, 85, 90]},
        {'name': 'Charlie Reyes', 'scores': [95, 92, 88, 91]},
    ]
    max_score_per_activity = 100
    total_possible = max_score_per_activity * len(activities)
    for student in students:
        total = sum(student['scores'])
        student['total'] = total
        percentage = (total / total_possible) * 100
        student['grade'] = compute_grade(percentage)
    summary_data = []
    for i in range(len(activities)):
        column_scores = [s['scores'][i] for s in students]
        avg = round(sum(column_scores) / len(column_scores), 1)
        summary_data.append(f'Avg: {avg}')

    # Get dashboard data
    classes = Class.objects.filter(is_archived=False)

    return render(request, 'faculty_laboratory/laboratory.html', {
        'class': class_data,
        'activities': activities,
        'students': students,
        'summary_data': summary_data,
        'classes': classes,  # Pass dashboard data
        'role' : 'faculty'
    })

def dashboard(request):
    classes = Class.objects.filter(is_archived=False)
    return render(request, 'faculty_laboratory/dashboard.html', {'classes': classes})

def compute_grade(percentage):
    if percentage >= 90:
        return 'A'
    elif percentage >= 80:
        return 'B'
    elif percentage >= 70:
        return 'C'
    elif percentage >= 60:
        return 'D'
    else:
        return 'F'