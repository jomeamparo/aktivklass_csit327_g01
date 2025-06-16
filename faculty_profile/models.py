from django.db import models

class FacultyProfile(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)

    class Meta:
        app_label = 'faculty_profile'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
