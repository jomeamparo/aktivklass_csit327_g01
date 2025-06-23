# faculty_attendance/views.py
from django.shortcuts import render
from core.models import Faculty_Attendance
from django.http import HttpResponse
import datetime
import openpyxl

def faculty_attendance_view(request):
    subject = request.GET.get('subject')
    date_filter_str = request.GET.get('date') # This will be 'YYYY-MM-DD' from the HTML input type="date"

    records = Faculty_Attendance.objects.all()

    if subject:
        records = records.filter(subject=subject)

    if date_filter_str:
        # No need for strptime here for filtering a DateField with a YYYY-MM-DD string
        # Django's ORM handles this efficiently.
        # If you were getting 'dd-mm-yyyy' from the frontend (e.g., via JS datepicker and type="text"),
        # you would do:
        # try:
        #     parsed_date = datetime.datetime.strptime(date_filter_str, '%d-%m-%Y').date()
        #     records = records.filter(date=parsed_date)
        # except ValueError:
        #     pass # Handle invalid date format
        records = records.filter(date=date_filter_str)

    # Handle Excel download
    if 'download' in request.GET:
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Attendance Records"
        # Ensure header matches your append order
        sheet.append(['ID Number', 'First Name', 'Last Name', 'Subject', 'Date', 'Status'])

        for record in records:
            sheet.append([
                record.id_number, # Added id_number here for consistency with your model
                record.first_name,
                record.last_name,
                record.subject,
                # For Excel, YYYY-MM-DD is generally better for data processing,
                # but if you specifically need DD-MM-YYYY in the Excel cell for presentation, change this:
                record.date.strftime('%d-%m-%Y'), # Changed to dd-mm-yyyy for Excel output
                record.status
            ])

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=attendance_report.xlsx'
        workbook.save(response)
        return response

    return render(request, 'faculty_attendance/faculty_attendance.html', {'records': records})