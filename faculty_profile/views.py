from django.shortcuts import render, redirect
from django.db import ProgrammingError, OperationalError
from .forms import FacultyProfileForm
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

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
        self.date_hired = "Not specified"
        self.website = "Not specified"
        self.birth_date = "Not specified"
    
    def save(self):
        # Mock save method - does nothing
        pass

def faculty_profile_view(request):
    profile = None
    try:
        from .models import FacultyProfile
        profile = FacultyProfile.objects.first()
        if not profile:
            profile = FacultyProfile.objects.create(first_name="John", last_name="Doe", department="CS") # Simplified for example
    except (ProgrammingError, OperationalError):
        if 'mock_profile' in request.session:
            profile = MockFacultyProfile()
            profile.__dict__.update(request.session['mock_profile'])
        else:
            profile = MockFacultyProfile()

    if request.method == 'POST':
        form = FacultyProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            if isinstance(profile, MockFacultyProfile):
                profile_data = {k: v for k, v in form.cleaned_data.items() if k != 'profile_picture'}

                if 'profile_picture' in request.FILES:
                    file = request.FILES['profile_picture']
                    fs = FileSystemStorage()
                    filename = fs.save(f'profile_pictures/{file.name}', file)
                    profile_data['profile_picture_url'] = fs.url(filename)
                
                request.session['mock_profile'] = profile_data
            else:
                form.save()
            
            messages.success(request, 'Your profile was updated successfully!')
            return redirect('faculty_profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = FacultyProfileForm(instance=profile)

    context = {
        'faculty': profile,
        'form': form,
        'role': 'faculty'
    }
    return render(request, 'faculty_profile/faculty_profile.html', context)
