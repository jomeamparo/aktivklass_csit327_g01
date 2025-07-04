from django.shortcuts import render, redirect
from django.db import ProgrammingError, OperationalError
from .forms import FacultyProfileForm
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
import datetime

class MockFacultyProfile:
    """Mock class to simulate FacultyProfile when database table doesn't exist"""
    def __init__(self):
        self.first_name = "John"
        self.last_name = "Doe"
        self.department = "Computer Science"
        self.email = "john.doe@cit.edu"
        self.contact_number = "09123456789"
        self.office_location = "N/A"
        self.profile_picture_url = None  # Use URL for session-based image
        self.bio = "No bio information provided."
        self.faculty_id = "FAC-001"
        self.position = "Professor"
        self.college = "College of Computer Studies"
        self.specialization = "Not specified"
        self.date_hired = ""  # Use empty string for date fields
        self.birth_date = ""  # Use empty string for date fields
        self.status = "Active"  # Valid default status
    
    def save(self):
        # Mock save method - does nothing
        pass

def faculty_profile_view(request):
    profile = None
    is_mock = False
    try:
        from core.models import FacultyProfile
        profile = FacultyProfile.objects.first()
        if not profile:
            profile = FacultyProfile.objects.create(first_name="John", last_name="Doe", department="CS") # Simplified for example
    except (ProgrammingError, OperationalError):
        is_mock = True
        # Clear session if mock_profile is invalid
        if 'mock_profile' in request.session:
            data = request.session['mock_profile']
            # Check for required fields and valid status
            required_fields = [
                'first_name', 'last_name', 'department', 'email', 'contact_number',
                'office_location', 'bio', 'faculty_id', 'position', 'college',
                'specialization', 'date_hired', 'birth_date', 'status'
            ]
            valid_statuses = ['Active', 'Busy', 'Offline']
            if not all(f in data for f in required_fields) or data.get('status') not in valid_statuses:
                request.session.pop('mock_profile', None)
                profile = MockFacultyProfile()
            else:
                profile = MockFacultyProfile()
                profile.__dict__.update(data)
        else:
            profile = MockFacultyProfile()

    if request.method == 'POST':
        if is_mock:
            # Use initial data for plain Form, not ModelForm
            form = FacultyProfileForm(request.POST, request.FILES, initial=profile.__dict__)
        else:
            form = FacultyProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            if is_mock:
                profile_data = {k: v for k, v in form.cleaned_data.items() if k != 'profile_picture'}
                # Convert date/datetime objects to string for session storage
                for key in ['birth_date', 'date_hired']:
                    if key in profile_data and isinstance(profile_data[key], (datetime.date, datetime.datetime)):
                        profile_data[key] = profile_data[key].isoformat()
                if 'profile_picture' in request.FILES:
                    file = request.FILES['profile_picture']
                    fs = FileSystemStorage()
                    filename = fs.save(f'profile_pictures/{file.name}', file)
                    profile_data['profile_picture_url'] = fs.url(filename)
                # Ensure status is always included
                if 'status' not in profile_data:
                    profile_data['status'] = getattr(profile, 'status', 'Active')
                request.session['mock_profile'] = profile_data
            else:
                form.save()
            messages.success(request, 'Your profile was updated successfully!')
            return redirect('faculty_profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        if is_mock:
            form = FacultyProfileForm(initial=profile.__dict__)
        else:
            form = FacultyProfileForm(instance=profile)

    context = {
        'faculty': profile,
        'form': form,
        'role': 'faculty'
    }
    return render(request, 'faculty_profile/faculty_profile.html', context)
