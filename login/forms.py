from django import forms
from django.core.validators import EmailValidator

class LoginForm(forms.Form):
    email = forms.Field(
        widget=forms.EmailInput(attrs={
            'class': 'form-control'
        }),
    )
    password = forms.CharField(
        initial='password123', 
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'form-control',
            'value': 'password123',
        }),
        min_length=6,
        error_messages={'required': 'Please enter your password.'}
    )
