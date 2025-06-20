from django import forms
from core.models import FacultyProfile

class FacultyProfileForm(forms.ModelForm):
    class Meta:
        model = FacultyProfile
        fields = [
            'first_name', 
            'last_name', 
            'department', 
            'email', 
            'contact_number',
            'office_location',
            'profile_picture',
            'bio'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'contact_number': forms.TextInput(attrs={'pattern': '[0-9]{11}', 'placeholder': '09XXXXXXXXX'}),
            'office_location': forms.TextInput(attrs={'placeholder': 'Building and Room Number'}),
        } 