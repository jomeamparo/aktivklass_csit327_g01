from django import forms
from core.models import Student
import re

class StudentProfileForm(forms.ModelForm):
    """
    Form for handling both Student and StudentProfile models
    Additional profile fields are added to this form
    """
    # Student model fields remain the same
    
    # Profile fields
    avatar = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        required=False
    )
    bio = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False
    )
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=False
    )
    website = forms.URLField(
        widget=forms.URLInput(attrs={'class': 'form-control'}),
        required=False
    )
    major = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    graduation_year = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=False
    )
    
    class Meta:
        model = Student
        fields = [
            'student_id', 'first_name', 'middle_name', 'last_name', 
            'email', 'phone_number', 'course', 'year', 'status'
        ]
        widgets = {
            'student_id': forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'course': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        """
        Initialize the form with both Student and StudentProfile instances
        """
        # Pop the profile instance before calling parent's __init__
        self.profile_instance = kwargs.pop('profile_instance', None)
        super().__init__(*args, **kwargs)
        
        # If we have a profile instance, populate the form with its data
        if self.profile_instance:
            self.fields['avatar'].initial = self.profile_instance.avatar
            self.fields['bio'].initial = self.profile_instance.bio
            self.fields['birth_date'].initial = self.profile_instance.birth_date
            self.fields['website'].initial = self.profile_instance.website
            self.fields['major'].initial = self.profile_instance.major
            self.fields['graduation_year'].initial = self.profile_instance.graduation_year
    
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
    
    def save(self, commit=True):
        """
        Save both the Student and StudentProfile models
        """
        # Save the Student model
        student = super().save(commit=commit)
        
        # Save the StudentProfile model
        if self.profile_instance:
            self.profile_instance.avatar = self.cleaned_data.get('avatar') or self.profile_instance.avatar
            self.profile_instance.bio = self.cleaned_data.get('bio')
            self.profile_instance.birth_date = self.cleaned_data.get('birth_date')
            self.profile_instance.website = self.cleaned_data.get('website')
            self.profile_instance.major = self.cleaned_data.get('major')
            self.profile_instance.graduation_year = self.cleaned_data.get('graduation_year')
            
            if commit:
                self.profile_instance.save()
        
        return student

class StudentStatusForm(forms.Form):
    """Form for updating just the student status"""
    status = forms.ChoiceField(
        choices=[('Available', 'Available'), ('Busy', 'Busy'), ('Offline', 'Offline')],
        widget=forms.Select(attrs={'class': 'form-control'})
    ) 