from django.shortcuts import render
from .models import Faculty_Attendance

def attendance_records(request):
    selected_class = request.GET.get('class')
    selected_date = request.GET.get('date')

    records = Faculty_Attendance.objects.all()

    if selected_class:
        records = records.filter(subject_class=selected_class)

    if selected_date:
        records = records.filter(date=selected_date)

    return render(request, 'attendance.html', {
        'records': records,
        'selected_class': selected_class,
        'selected_date': selected_date,
    })
