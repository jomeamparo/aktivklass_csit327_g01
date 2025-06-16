from django.db import models
from django.contrib.auth.models import User

class FacultySettings(models.Model):
    faculty = models.OneToOneField(User, on_delete=models.CASCADE, related_name='settings')
    
    # General Settings
    dark_mode = models.BooleanField(default=False)
    language = models.CharField(max_length=10, default='en')
    timezone = models.CharField(max_length=50, default='Asia/Manila')
    
    # Notification Settings
    notif_assignments = models.BooleanField(default=True)
    notif_announcements = models.BooleanField(default=True)
    notif_messages = models.BooleanField(default=True)
    
    # Faculty Specific Settings
    course_notifications = models.BooleanField(default=True)
    grading_system = models.CharField(max_length=20, default='letter')
    comm_email = models.BooleanField(default=True)
    comm_sms = models.BooleanField(default=False)
    comm_in_app = models.BooleanField(default=True)
    allowed_file_types = models.CharField(max_length=255, default='pdf,docx,doc')
    max_file_size = models.IntegerField(default=10)  # in MB
    
    # Security Settings
    password_strength = models.CharField(max_length=20, default='medium')
    mfa_enabled = models.BooleanField(default=False)
    recovery_email = models.EmailField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Faculty Settings'
        verbose_name_plural = 'Faculty Settings'
    
    def __str__(self):
        return f"Settings for {self.faculty.username}"
    
    def to_dict(self):
        return {
            'id': self.id,
            'faculty_id': self.faculty.id,
            'dark_mode': self.dark_mode,
            'language': self.language,
            'timezone': self.timezone,
            'notif_assignments': self.notif_assignments,
            'notif_announcements': self.notif_announcements,
            'notif_messages': self.notif_messages,
            'course_notifications': self.course_notifications,
            'grading_system': self.grading_system,
            'comm_email': self.comm_email,
            'comm_sms': self.comm_sms,
            'comm_in_app': self.comm_in_app,
            'allowed_file_types': self.allowed_file_types,
            'max_file_size': self.max_file_size,
            'password_strength': self.password_strength,
            'mfa_enabled': self.mfa_enabled,
            'recovery_email': self.recovery_email,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
