from django.shortcuts import render
from .models import FacultyProfile
from .forms import FacultyProfileForm

def faculty_profile_view(request):
    # Create a default profile if none exists
    profile = FacultyProfile.objects.first()
    if not profile:
        profile = FacultyProfile.objects.create(
            first_name="John",
            last_name="Doe",
            department="Computer Science",
            email="john.doe@example.com",
            bio="Welcome to my profile!"
        )

    form = FacultyProfileForm(instance=profile)

    context = {
        'faculty': profile,
        'form': form,
        'role': 'faculty'
    }
    return render(request, 'faculty_profile/faculty_profile.html', context)
