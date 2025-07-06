from django.shortcuts import render
from core.models import Student, Faculty, AdminUser
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from .models import SeatworkRecord
import csv
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

def user_context_processor(request):
    """
    Context processor to add user information to all templates.
    This ensures the sidebar shows the correct email for the logged-in user.
    """
    context = {'avatar_url': None}
    
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        
        # Try to get the user from Student model
        student = Student.objects.filter(student_id=user_id).first()
        if student:
            context['fullname'] = f"{student.first_name} {student.last_name}"
            context['email'] = student.email
            context['role'] = 'student'
            if hasattr(student, 'profile') and student.profile.avatar:
                context['avatar_url'] = student.profile.avatar.url
            return context
            
        # Try to get the user from Faculty model
        faculty = Faculty.objects.filter(faculty_id=user_id).first()
        if faculty:
            context['fullname'] = f"{faculty.first_name} {faculty.last_name}"
            context['email'] = faculty.email
            context['role'] = 'faculty'
            return context
            
        # Try to get the user from AdminUser model
        admin = AdminUser.objects.filter(employee_id=user_id).first()
        if admin:
            context['fullname'] = f"{admin.first_name} {admin.last_name}"
            context['email'] = admin.email
            context['role'] = 'admin'
            return context
    
    # Default values if no user is found or not logged in
    context['fullname'] = "Guest User"
    context['email'] = ""
    context['role'] = 'guest'
    
    return context
from django.http import HttpResponse

# Create your views here.

def test_profile(request):
    """Test view to set up session data for profile testing"""
    # Set up mock faculty session data
    request.session['role'] = 'faculty'
    request.session['user_id'] = 'FAC-001'
    
    # Set up mock profile data
    request.session['mock_profile'] = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@cit.edu',
        'department': 'Computer Science',
        'contact_number': '09123456789',
        'office_location': 'Room 101',
        'profile_picture_url': None,
        'bio': 'Experienced faculty member',
        'faculty_id': 'FAC-001',
        'position': 'Professor',
        'college': 'College of Computer Studies',
        'specialization': 'Software Engineering',
        'date_hired': '2020-01-01',
        'website': 'https://example.com',
        'birth_date': '1985-01-01'
    }
    
    return HttpResponse("Session data set up for testing. <a href='/dashboard_teacher/'>Go to Dashboard</a>")

def records_list(request):
    # Render the page with all records
    records = SeatworkRecord.objects.all().order_by('-date')
    return render(request, 'yourapp/records.html', {'records': records})

@csrf_exempt
def api_records(request):
    # API endpoint for CRUD operations (expects JSON)

    if request.method == 'GET':
        # Return all records as JSON
        records = list(SeatworkRecord.objects.values())
        return JsonResponse(records, safe=False)

    elif request.method == 'POST':
        # Create new record
        data = json.loads(request.body)
        record = SeatworkRecord.objects.create(
            name=data['name'],
            activity=data['activity'],
            score=data['score'],
            status=data['status'],
            date=data['date']
        )
        return JsonResponse({'id': record.id})

    elif request.method == 'PUT':
        # Update existing record
        data = json.loads(request.body)
        record = get_object_or_404(SeatworkRecord, pk=data['id'])
        record.name = data['name']
        record.activity = data['activity']
        record.score = data['score']
        record.status = data['status']
        record.date = data['date']
        record.save()
        return JsonResponse({'updated': True})

    elif request.method == 'DELETE':
        data = json.loads(request.body)
        record = get_object_or_404(SeatworkRecord, pk=data['id'])
        record.delete()
        return JsonResponse({'deleted': True})

def export_csv(request):
    records = SeatworkRecord.objects.all().order_by('-date')
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="student_seatwork_records.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Name', 'Activity', 'Score', 'Status', 'Date'])
    
    for record in records:
        writer.writerow([record.name, record.activity, record.score, record.status, record.date])
    
    return response