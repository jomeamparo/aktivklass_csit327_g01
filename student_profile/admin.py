from django.contrib import admin
from core.models import StudentProfile

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('student', 'major', 'graduation_year', 'phone_verified', 'last_updated')
    list_filter = ('phone_verified', 'major')
    search_fields = ('student__first_name', 'student__last_name', 'student__email', 'major')
    readonly_fields = ('last_updated',)
