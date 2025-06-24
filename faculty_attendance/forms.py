from django import forms
from .models import FacultyAttendance, AttendanceSchedule
from core.models import Class

class FacultyAttendanceForm(forms.ModelForm):
    class_instance = forms.ModelChoiceField(
        queryset=Class.objects.all(),
        empty_label="Select a class",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = FacultyAttendance
        fields = ['class_instance', 'status', 'remarks']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class AttendanceScheduleForm(forms.ModelForm):
    class Meta:
        model = AttendanceSchedule
        fields = ['class_instance', 'day_of_week', 'start_time', 'end_time', 'is_active']
        widgets = {
            'class_instance': forms.Select(attrs={'class': 'form-control'}),
            'day_of_week': forms.Select(attrs={'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        } 