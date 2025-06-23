from django.db import models
from django.conf import settings

class FacultyProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    office_location = models.CharField(max_length=200, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(blank=True)
    faculty_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    college = models.CharField(max_length=100, blank=True, null=True)
    specialization = models.CharField(max_length=100, blank=True, null=True)
    date_hired = models.DateField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
