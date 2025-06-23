from django import forms

class FacultyProfileForm(forms.Form):
    default_attrs = {'class': 'w-full px-3 py-2 text-gray-700 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500'}
    
    first_name = forms.CharField(widget=forms.TextInput(attrs=default_attrs))
    last_name = forms.CharField(widget=forms.TextInput(attrs=default_attrs))
    department = forms.CharField(widget=forms.TextInput(attrs=default_attrs))
    email = forms.EmailField(widget=forms.EmailInput(attrs=default_attrs))
    contact_number = forms.CharField(required=False, widget=forms.TextInput(attrs={**default_attrs, 'placeholder': '09XXXXXXXXX'}))
    office_location = forms.CharField(required=False, widget=forms.TextInput(attrs={**default_attrs, 'placeholder': 'Building and Room Number'}))
    profile_picture = forms.ImageField(required=False)
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={**default_attrs, 'rows': 3}))
    faculty_id = forms.CharField(required=False, widget=forms.TextInput(attrs=default_attrs))
    position = forms.CharField(required=False, widget=forms.TextInput(attrs=default_attrs))
    college = forms.CharField(required=False, widget=forms.TextInput(attrs=default_attrs))
    specialization = forms.CharField(required=False, widget=forms.TextInput(attrs=default_attrs))
    date_hired = forms.CharField(required=False, widget=forms.TextInput(attrs=default_attrs))
    website = forms.CharField(required=False, widget=forms.URLInput(attrs=default_attrs))
    birth_date = forms.CharField(required=False, widget=forms.TextInput(attrs={**default_attrs, 'placeholder': 'YYYY-MM-DD'}))
    
    def __init__(self, *args, **kwargs):
        instance = kwargs.pop('instance', None)
        initial = kwargs.pop('initial', None)
        
        if instance:
            initial = instance.__dict__

        super().__init__(*args, initial=initial, **kwargs)
        
        if instance:
            # Manually set file field initial value if it exists
            if hasattr(instance, 'profile_picture') and instance.profile_picture:
                self.fields['profile_picture'].initial = instance.profile_picture

            self.fields['first_name'].initial = getattr(instance, 'first_name', '')
            self.fields['last_name'].initial = getattr(instance, 'last_name', '')
            self.fields['department'].initial = getattr(instance, 'department', '')
            self.fields['email'].initial = getattr(instance, 'email', '')
            self.fields['contact_number'].initial = getattr(instance, 'contact_number', '')
            self.fields['office_location'].initial = getattr(instance, 'office_location', '')
            self.fields['bio'].initial = getattr(instance, 'bio', '')
            self.fields['faculty_id'].initial = getattr(instance, 'faculty_id', '')
            self.fields['position'].initial = getattr(instance, 'position', '')
            self.fields['college'].initial = getattr(instance, 'college', '')
            self.fields['specialization'].initial = getattr(instance, 'specialization', '')
            self.fields['date_hired'].initial = getattr(instance, 'date_hired', '')
            self.fields['website'].initial = getattr(instance, 'website', '')
            self.fields['birth_date'].initial = getattr(instance, 'birth_date', '') 