from django.urls import path
from .views import faculty_seatworkSubmission_views

urlpatterns = [
    path('', faculty_seatworkSubmission_views, name='faculty_seatworkSubmission'),
]