from django.apps import AppConfig


class FacultyProfileConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'faculty_profile'

    def ready(self):
        import faculty_profile.signals
