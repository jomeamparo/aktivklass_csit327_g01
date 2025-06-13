from django.urls import path
from .views import faculty_settings

urlpatterns = [
    path('', faculty_settings, name='faculty_settings'),
]
