from django.urls import path
from .views import faculty_profile_view

urlpatterns = [
    path('', faculty_profile_view, name='faculty_profile'),
]
