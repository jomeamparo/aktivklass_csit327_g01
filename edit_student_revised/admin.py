from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'first_name', 'last_name', 'email', 'is_disabled')
    list_filter = ('is_disabled',)
    search_fields = ('student_id', 'first_name', 'last_name', 'email')
    ordering = ('student_id',)
