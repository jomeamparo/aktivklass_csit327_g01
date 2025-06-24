from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from core.models import FacultyProfile
from django.contrib.auth.models import User

@receiver(user_logged_in)
def create_faculty_profile_on_login(sender, user, request, **kwargs):
    if not FacultyProfile.objects.exists():
        FacultyProfile.objects.create(
            first_name=user.first_name or "First",
            last_name=user.last_name or "Last",
            email=user.email,
            department="Department",
            bio="Welcome to my profile!"
        ) 