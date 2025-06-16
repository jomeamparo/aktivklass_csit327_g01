from django.db import models
from core.models import Faculty
import uuid

class PasswordResetToken(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)