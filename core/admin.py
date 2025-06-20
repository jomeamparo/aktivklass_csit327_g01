from django.contrib import admin
from core.models import FacultyProfile

@admin.register(FacultyProfile)
class FacultyProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'department', 'email')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('department',)

