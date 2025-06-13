from django import forms
from .models import FacultyProfile

class FacultyProfileForm(forms.ModelForm):
    class Meta:
        model = FacultyProfile
        fields = ['first_name', 'last_name', 'department', 'email', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        } 