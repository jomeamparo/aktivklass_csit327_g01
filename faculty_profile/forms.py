from django import forms
from core.models import FacultyProfile

class FacultyProfileForm(forms.ModelForm):
    class Meta:
        model = FacultyProfile
        fields = [
            'first_name', 'last_name', 'department', 'email', 'contact_number',
            'office_location', 'profile_picture', 'bio', 'faculty_id', 'position',
            'college', 'specialization', 'date_hired', 'birth_date', 'status'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 text-gray-700 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 text-gray-700 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500'}),
            'department': forms.TextInput(attrs={'class': 'w-full px-3 py-2 text-gray-700 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-3 py-2 text-gray-700 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500'}),
            'contact_number': forms.TextInput(attrs={'class': 'w-full px-3 py-2 text-gray-700 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500', 'placeholder': '09XXXXXXXXX'}),
            'office_location': forms.TextInput(attrs={'class': 'w-full px-3 py-2 text-gray-700 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500', 'placeholder': 'Building and Room Number'}),
            'bio': forms.Textarea(attrs={'class': 'w-full px-3 py-2 text-gray-700 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500', 'rows': 3}),
            'faculty_id': forms.TextInput(attrs={'class': 'w-full px-3 py-2 text-gray-700 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500'}),
            'position': forms.TextInput(attrs={'class': 'w-full px-3 py-2 text-gray-700 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500'}),
            'college': forms.TextInput(attrs={'class': 'w-full px-3 py-2 text-gray-700 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500'}),
            'specialization': forms.TextInput(attrs={'class': 'w-full px-3 py-2 text-gray-700 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500'}),
            'date_hired': forms.DateInput(attrs={'class': 'w-full px-3 py-2 text-gray-700 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500', 'placeholder': 'YYYY-MM-DD'}),
            'birth_date': forms.DateInput(attrs={'class': 'w-full px-3 py-2 text-gray-700 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500', 'placeholder': 'YYYY-MM-DD'}),
            'status': forms.Select(attrs={'class': 'w-full px-3 py-2 text-gray-700 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500'}),
        } 