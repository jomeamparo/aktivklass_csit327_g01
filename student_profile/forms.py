from django import forms
import re
# from core.models import Student # Import Student model

class StudentProfileForm(forms.Form):
    student_id = forms.CharField(max_length=20, disabled=True, help_text="Student ID cannot be changed.")
    first_name = forms.CharField(max_length=100)
    middle_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=15, required=False, help_text="Enter 10 to 15 digits only.")
    course = forms.CharField(max_length=50, required=False)
    year = forms.CharField(max_length=50, required=False)
    status = forms.ChoiceField(choices=[('Available', 'Available'), ('Busy', 'Busy'), ('Offline', 'Offline')])

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and not re.match(r'^\d{10,15}$', phone_number):
            raise forms.ValidationError('Phone number must be between 10 and 15 digits and contain only numbers.')
        return phone_number

    def clean_student_id(self):
        student_id = self.cleaned_data.get('student_id')
        if student_id and not re.match(r'^[a-zA-Z0-9]+$', student_id):
            raise forms.ValidationError('Student ID must be alphanumeric.')
        return student_id 