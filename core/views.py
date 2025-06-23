from django.shortcuts import render
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
