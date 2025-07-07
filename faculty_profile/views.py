from django.shortcuts import render, redirect
from django.db import ProgrammingError, OperationalError
from .forms import FacultyProfileForm
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
import datetime
from core.models import Faculty, FacultyProfile  # ✅ Make sure FacultyProfile is imported
 
class MockFacultyProfile:
    """Mock class to simulate FacultyProfile when database table doesn't exist"""
    def __init__(self):
        self.first_name = "John"
        self.last_name = "Doe"
        self.department = "Computer Science"
        self.email = "john.doe@cit.edu"
        self.contact_number = "09123456789"
        self.office_location = "N/A"
        self.profile_picture_url = None
        self.bio = "No bio information provided."
        self.profile_faculty_id = "FAC-001"
        self.position = "Professor"
        self.college = "College of Computer Studies"
        self.specialization = "Not specified"
        self.date_hired = ""
        self.birth_date = ""
        self.status = "Active"
 
    def save(self):
        pass
 
def faculty_profile_view(request):
    profile = None
    is_mock = False
 
    # Session-based authentication
    user_id = request.session.get('user_id')
    role = request.session.get('role')
 
    if not user_id or role != 'faculty':
        messages.error(request, 'Please log in as a faculty member to access your profile.')
        return redirect('login')
 
    try:
        # Try to fetch profile using faculty_id (CharField)
        profile = FacultyProfile.objects.filter(faculty_id=user_id).first()
 
        if not profile:
            # Try to create a profile using Faculty model data
            try:
                faculty = Faculty.objects.get(faculty_id=user_id)
                profile = FacultyProfile.objects.create(
                    faculty_id=user_id,
                    first_name=faculty.first_name,
                    last_name=faculty.last_name,
                    department=faculty.department_name,
                    email=faculty.email
                )
            except Faculty.DoesNotExist:
                pass  # Will use mock fallback later
 
    except (ProgrammingError, OperationalError):
        is_mock = True
 
    # Fallback to mock profile
    if not profile:
        is_mock = True
        if 'mock_profile' in request.session:
            data = request.session['mock_profile']
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
 
    # Handle form submission
    if request.method == 'POST':
        if is_mock:
            form = FacultyProfileForm(request.POST, request.FILES, initial=profile.__dict__)
        else:
            form = FacultyProfileForm(request.POST, request.FILES, instance=profile)
 
        if form.is_valid():
            if is_mock:
                profile_data = {k: v for k, v in form.cleaned_data.items() if k != 'profile_picture'}
 
                # Convert date/datetime to strings for session storage
                for key in ['birth_date', 'date_hired']:
                    if isinstance(profile_data.get(key), (datetime.date, datetime.datetime)):
                        profile_data[key] = profile_data[key].isoformat()
 
                # Handle file upload
                if 'profile_picture' in request.FILES:
                    file = request.FILES['profile_picture']
                    fs = FileSystemStorage()
                    filename = fs.save(f'profile_pictures/{file.name}', file)
                    profile_data['profile_picture_url'] = fs.url(filename)
 
                profile_data.setdefault('status', getattr(profile, 'status', 'Active'))
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