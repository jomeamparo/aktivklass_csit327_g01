from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from core.models import Student, Class, Attendance

from core.models import ActivityRecord, QuizGrade

import openpyxl
from openpyxl.utils import get_column_letter

# Export attendance to Excel
from django.utils.encoding import smart_str

def export_attendance_excel(request):
    student_id = request.session.get('user_id')
    role = request.session.get('role')
    if role != 'student' or not student_id:
        return HttpResponse('Unauthorized', status=401)
    try:
        student = Student.objects.get(student_id=student_id)
    except Student.DoesNotExist:
        return HttpResponse('Student not found', status=404)
    status_filter = request.GET.get('status')
    attendance_records = Attendance.objects.filter(student=student).select_related('class_obj')
    if status_filter in ['Present', 'Absent', 'Late']:
        attendance_records = attendance_records.filter(status=status_filter)
    # Create workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Attendance Records'
    headers = ['Date', 'Class', 'Status', 'Feedback']
    ws.append(headers)
    for record in attendance_records:
        ws.append([
            record.date.strftime('%Y-%m-%d'),
            str(record.class_obj),
            record.status,
            record.feedback or ''
        ])
    # Set column widths
    for i, col in enumerate(headers, 1):
        ws.column_dimensions[get_column_letter(i)].width = 20
    # Prepare response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    filename = f"attendance_{student_id}.xlsx"
    response['Content-Disposition'] = f'attachment; filename={smart_str(filename)}'
    wb.save(response)
    return response

import json

def student_attendance_dashboard(request):
    student_id = request.session.get('user_id')
    role = request.session.get('role')
    if role != 'student' or not student_id:
        return render(request, 'error.html', {'message': 'You are not logged in as a student.'})
    try:
        student = Student.objects.get(student_id=student_id)
    except Student.DoesNotExist:
        return render(request, 'error.html', {'message': 'No student record found for this account.'})
    attendance_records = Attendance.objects.filter(student=student).select_related('class_obj')
    total_attendance = attendance_records.count()
    present_count = attendance_records.filter(status='Present').count()
    absent_count = attendance_records.filter(status='Absent').count()

    # Compute stats per subject/class
    stats_dict = {}
    for record in attendance_records:
        class_label = str(record.class_obj)  # You can use record.class_obj.subject if available
        if class_label not in stats_dict:
            stats_dict[class_label] = {'subject': class_label, 'present': 0, 'absent': 0}
        if record.status == 'Present':
            stats_dict[class_label]['present'] += 1
        elif record.status == 'Absent':
            stats_dict[class_label]['absent'] += 1
    attendance_stats = list(stats_dict.values())

    # Calculate attendance rate (handle division by zero)
    attendance_rate = round((present_count / total_attendance * 100), 1) if total_attendance > 0 else 0

    context = {
        'total_attendance': total_attendance,
        'present_count': present_count,
        'absent_count': absent_count,
        'attendance_rate': attendance_rate,
        'attendance_stats': attendance_stats,
        'attendance_stats_json': json.dumps(attendance_stats),  # For the chart
        'role': role,
        'fullname': f"{student.first_name} {student.last_name}",
        'email': student.email,
        'avatar_url': student.profile.avatar.url if hasattr(student, 'profile') and student.profile.avatar else None,
    }
    return render(request, 'attendance_student/student_attendance_dashboard.html', context)

def student_attendance_present(request):
    student_id = request.session.get('user_id')
    role = request.session.get('role')
    if role != 'student' or not student_id:
        return render(request, 'error.html', {'message': 'You are not logged in as a student.'})
    try:
        student = Student.objects.get(student_id=student_id)
    except Student.DoesNotExist:
        return render(request, 'error.html', {'message': 'No student record found for this account.'})
    attendance_records = Attendance.objects.filter(student=student, status='Present').select_related('class_obj')
    context = {
        'attendance_records': attendance_records,
        'filter_label': 'Present',
        'role': role,
        'fullname': f"{student.first_name} {student.last_name}",
        'email': student.email,
        'avatar_url': student.profile.avatar.url if hasattr(student, 'profile') and student.profile.avatar else None,
    }
    return render(request, 'attendance_student/attendance_detail.html', context)

def student_attendance_absent(request):
    student_id = request.session.get('user_id')
    role = request.session.get('role')
    if role != 'student' or not student_id:
        return render(request, 'error.html', {'message': 'You are not logged in as a student.'})
    try:
        student = Student.objects.get(student_id=student_id)
    except Student.DoesNotExist:
        return render(request, 'error.html', {'message': 'No student record found for this account.'})
    attendance_records = Attendance.objects.filter(student=student, status='Absent').select_related('class_obj')
    context = {
        'attendance_records': attendance_records,
        'filter_label': 'Absent',
        'role': role,
        'fullname': f"{student.first_name} {student.last_name}",
        'email': student.email,
        'avatar_url': student.profile.avatar.url if hasattr(student, 'profile') and student.profile.avatar else None,
    }
    return render(request, 'attendance_student/attendance_detail.html', context)

def student_attendance_all(request):
    student_id = request.session.get('user_id')
    role = request.session.get('role')
    if role != 'student' or not student_id:
        return render(request, 'error.html', {'message': 'You are not logged in as a student.'})
    try:
        student = Student.objects.get(student_id=student_id)
    except Student.DoesNotExist:
        return render(request, 'error.html', {'message': 'No student record found for this account.'})
    attendance_records = Attendance.objects.filter(student=student).select_related('class_obj')
    context = {
        'attendance_records': attendance_records,
        'filter_label': 'All',
        'role': role,
        'fullname': f"{student.first_name} {student.last_name}",
        'email': student.email,
        'avatar_url': student.profile.avatar.url if hasattr(student, 'profile') and student.profile.avatar else None,
    }
    return render(request, 'attendance_student/attendance_detail.html', context)

def student_view_attendance(request):
    student_id = request.session.get('user_id')
    role = request.session.get('role')
    if role != 'student' or not student_id:
        return render(request, 'error.html', {'message': 'You are not logged in as a student.'})
    try:
        student = Student.objects.get(student_id=student_id)
    except Student.DoesNotExist:
        return render(request, 'error.html', {'message': 'No student record found for this account.'})
    attendance_records = Attendance.objects.filter(student=student).select_related('class_obj')
    total_attendance = attendance_records.count()
    present_count = attendance_records.filter(status='Present').count()
    absent_count = attendance_records.filter(status='Absent').count()
    context = {
        'attendance_records': attendance_records,
        'total_attendance': total_attendance,
        'present_count': present_count,
        'absent_count': absent_count,
        'role': role,
        'fullname': f"{student.first_name} {student.last_name}",
        'email': student.email,
        'avatar_url': student.profile.avatar.url if hasattr(student, 'profile') and student.profile.avatar else None,
    }
    return render(request, 'attendance_student/student_attendance.html', context)

def student_dashboard(request):
    student_id = request.session.get('user_id')
    role = request.session.get('role')
    if role != 'student' or not student_id:
        return render(request, 'error.html', {'message': 'You are not logged in as a student.'})
    try:
        student = Student.objects.get(student_id=student_id)
    except Student.DoesNotExist:
        return render(request, 'error.html', {'message': 'No student record found for this account.'})

    # Attendance Rate
    total_attendance = Attendance.objects.filter(student=student).count()
    present_attendance = Attendance.objects.filter(student=student, status='Present').count()
    attendance_rate = round((present_attendance / total_attendance) * 100, 1) if total_attendance > 0 else 0

    # Average Grade (from QuizGrade and ActivityRecord)
    quiz_grades = QuizGrade.objects.filter(student=student)
    activity_records = ActivityRecord.objects.filter(student=student)
    quiz_scores = list(quiz_grades.values_list('percentage', flat=True))
    activity_scores = [((rec.score / rec.perfect_score) * 100) for rec in activity_records if rec.score is not None and rec.perfect_score]
    all_scores = quiz_scores + activity_scores
    average_grade = round(sum(all_scores) / len(all_scores), 1) if all_scores else None

    # Most Recent Grade (QuizGrade)
    recent_grade = quiz_grades.order_by('-graded_at').first()

    # Recent Activities (ActivityRecord, last 5)
    recent_activities = activity_records.order_by('-date')[:5]

    context = {
        'attendance_rate': attendance_rate,
        'average_grade': average_grade,
        'recent_grade': recent_grade,
        'recent_activities': recent_activities,
        'role': role,
        'fullname': f"{student.first_name} {student.last_name}",
        'email': student.email,
        'avatar_url': student.profile.avatar.url if hasattr(student, 'profile') and student.profile.avatar else None,
    }
    return render(request, 'attendance_student/student_dashboard.html', context)

from django.views.decorators.http import require_GET

@require_GET
def student_attendance_subject_detail(request):
    student_id = request.session.get('user_id')
    role = request.session.get('role')
    subject = request.GET.get('subject')
    if role != 'student' or not student_id or not subject:
        return render(request, 'error.html', {'message': 'Invalid request.'})
    try:
        student = Student.objects.get(student_id=student_id)
    except Student.DoesNotExist:
        return render(request, 'error.html', {'message': 'No student record found for this account.'})
    attendance_records = Attendance.objects.filter(student=student, class_obj__subject_name=subject).select_related('class_obj')
    present_count = attendance_records.filter(status='Present').count()
    absent_count = attendance_records.filter(status='Absent').count()
    context = {
        'subject': subject,
        'attendance_records': attendance_records,
        'present_count': present_count,
        'absent_count': absent_count,
        'role': role,
        'fullname': f"{student.first_name} {student.last_name}",
        'email': student.email,
        'avatar_url': student.profile.avatar.url if hasattr(student, 'profile') and student.profile.avatar else None,
    }
    return render(request, 'attendance_student/attendance_subject_detail.html', context)

def student_results_dashboard(request):
    import json
    from collections import defaultdict
    from django.db.models import Avg
    student_id = request.session.get('user_id')
    role = request.session.get('role')
    if role != 'student' or not student_id:
        return render(request, 'error.html', {'message': 'You are not logged in as a student.'})
    try:
        student = Student.objects.get(student_id=student_id)
    except Student.DoesNotExist:
        return render(request, 'error.html', {'message': 'No student record found for this account.'})
    from core.models import ActivityRecord
    activity_records = ActivityRecord.objects.filter(student=student).select_related('enrollment__enrolled_class')

    # Aggregate by subject
    subject_stats = {}
    subject_charts = {}
    passing_threshold = 60.0

    # Organize records by subject
    subject_map = defaultdict(list)
    for rec in activity_records:
        subject = rec.enrollment.enrolled_class.subject_name
        subject_map[subject].append(rec)

    for subject, records in subject_map.items():
        total = len(records)
        avg = round(sum([(r.score or 0) / (r.perfect_score or 100) * 100 for r in records]) / total, 1) if total else 0
        passed = sum(1 for r in records if r.score is not None and r.perfect_score and (r.score / r.perfect_score * 100) >= passing_threshold)
        failed = sum(1 for r in records if r.score is not None and r.perfect_score and (r.score / r.perfect_score * 100) < passing_threshold)
        subject_stats[subject] = {
            'average': avg,
            'total': total,
            'passed': passed,
            'failed': failed,
        }
        subject_charts[subject] = {
            'passed': passed,
            'failed': failed,
        }

    # For template: lists of dicts for cards, and chart data as JSON
    cards = [{'subject': s, 'average': d['average'], 'total': d['total']} for s, d in subject_stats.items()]
    chart_subjects = list(subject_charts.keys())
    chart_passed = [subject_charts[s]['passed'] for s in chart_subjects]
    chart_failed = [subject_charts[s]['failed'] for s in chart_subjects]

    context = {
        'cards': cards,
        'chart_subjects': json.dumps(chart_subjects),
        'chart_passed': json.dumps(chart_passed),
        'chart_failed': json.dumps(chart_failed),
        'role': role,
        'fullname': f"{student.first_name} {student.last_name}",
        'email': student.email,
        'avatar_url': student.profile.avatar.url if hasattr(student, 'profile') and student.profile.avatar else None,
    }
    return render(request, 'attendance_student/student_results_dashboard.html', context)

def student_view_results(request):
    student_id = request.session.get('user_id')
    role = request.session.get('role')
    if role != 'student' or not student_id:
        return render(request, 'error.html', {'message': 'You are not logged in as a student.'})
    try:
        student = Student.objects.get(student_id=student_id)
    except Student.DoesNotExist:
        return render(request, 'error.html', {'message': 'No student record found for this account.'})

    # Import models locally to avoid circular import if needed
    from core.models import ActivityRecord
    from core.models import QuizGrade

    # Fetch all activity records for this student
    activity_records = ActivityRecord.objects.filter(student=student)
    # Fetch all quiz grades for this student
    quiz_grades = QuizGrade.objects.filter(student=student)

    context = {
        'activity_records': activity_records,
        'quiz_grades': quiz_grades,
        'role': role,
        'fullname': f"{student.first_name} {student.last_name}",
        'email': student.email,
        'avatar_url': student.profile.avatar.url if hasattr(student, 'profile') and student.profile.avatar else None,
    }
    return render(request, 'attendance_student/student_results.html', context)
