from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from core.models import Faculty, Class
from .models import FacultyAttendance, AttendanceSchedule
from .forms import FacultyAttendanceForm, AttendanceScheduleForm
from datetime import datetime, timedelta

@login_required
def faculty_attendance_view(request):
    # Get the faculty member
    faculty = get_object_or_404(Faculty, email=request.user.email)
    
    # Get all classes for this faculty
    classes = Class.objects.filter(enrollment__faculty=faculty).distinct()
    
    # Get today's attendance records
    today = timezone.now().date()
    attendance_records = FacultyAttendance.objects.filter(
        faculty=faculty,
        date=today
    ).select_related('class_instance')
    
    # Get attendance schedules
    schedules = AttendanceSchedule.objects.filter(
        class_instance__in=classes,
        is_active=True
    ).select_related('class_instance')
    
    # Handle form submission
    if request.method == 'POST':
        form = FacultyAttendanceForm(request.POST)
        if form.is_valid():
            class_id = request.POST.get('class_instance')
            class_instance = get_object_or_404(Class, id=class_id)
            
            # Check if attendance already exists for today
            attendance, created = FacultyAttendance.objects.get_or_create(
                faculty=faculty,
                class_instance=class_instance,
                date=today,
                defaults={
                    'time_in': timezone.now().time(),
                    'status': form.cleaned_data['status'],
                    'remarks': form.cleaned_data['remarks']
                }
            )
            
            if not created:
                attendance.status = form.cleaned_data['status']
                attendance.remarks = form.cleaned_data['remarks']
                attendance.save()
            
            messages.success(request, 'Attendance recorded successfully!')
            return redirect('faculty_attendance')
    else:
        form = FacultyAttendanceForm()
    
    context = {
        'faculty': faculty,
        'classes': classes,
        'attendance_records': attendance_records,
        'schedules': schedules,
        'form': form,
        'today': today,
        'role': 'faculty'
    }
    return render(request, 'faculty_attendance/faculty_attendance.html', context)

@login_required
def mark_time_out(request, attendance_id):
    attendance = get_object_or_404(FacultyAttendance, id=attendance_id, faculty__email=request.user.email)
    
    if not attendance.time_out:
        attendance.time_out = timezone.now().time()
        attendance.save()
        messages.success(request, 'Time out recorded successfully!')
    
    return redirect('faculty_attendance')

@login_required
def attendance_history(request):
    faculty = get_object_or_404(Faculty, email=request.user.email)
    
    # Get date range from request or default to current month
    today = timezone.now().date()
    start_date = request.GET.get('start_date', today.replace(day=1))
    end_date = request.GET.get('end_date', today)
    
    # Convert string dates to datetime objects if they're strings
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    
    # Get attendance records for the date range
    attendance_records = FacultyAttendance.objects.filter(
        faculty=faculty,
        date__range=[start_date, end_date]
    ).select_related('class_instance').order_by('-date', '-time_in')
    
    context = {
        'faculty': faculty,
        'attendance_records': attendance_records,
        'start_date': start_date,
        'end_date': end_date,
        'role': 'faculty'
    }
    return render(request, 'faculty_attendance/attendance_history.html', context)
