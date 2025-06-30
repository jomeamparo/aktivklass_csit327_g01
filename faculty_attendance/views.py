from django.shortcuts import render
from django.http import HttpResponse
from core.models import Faculty_Attendance
import datetime
import openpyxl

def faculty_attendance_view(request):
    subject = request.GET.get('subject')
    date_filter_str = request.GET.get('date')

    # Get all attendance records
    records = Faculty_Attendance.objects.all()

    # Filter by subject
    if subject:
        records = records.filter(subject__iexact=subject)

    # Filter by date
    if date_filter_str:
        try:
            parsed_date = datetime.datetime.strptime(date_filter_str, '%Y-%m-%d').date()
            records = records.filter(date=parsed_date)
        except ValueError:
            pass  # Ignore invalid date formats

    # Handle download request
    if 'download' in request.GET:
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Attendance Records"

        # Add headers
        sheet.append(['ID Number', 'First Name', 'Last Name', 'Subject', 'Date', 'Status'])

        # Add data rows
        for record in records:
            sheet.append([
                record.id_number,
                record.first_name,
                record.last_name,
                record.subject,
                record.date.strftime('%Y-%m-%d'),
                record.status
            ])

        # Return Excel response
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=attendance_report.xlsx'
        workbook.save(response)
        return response

    # Render the attendance page
    return render(request, 'faculty_attendance/faculty_attendance.html', {
        'records': records,
        'selected_subject': subject or '',
        'selected_date': date_filter_str or '',
        'role': 'faculty',
    })
