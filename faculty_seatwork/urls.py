from django.urls import path
from .views import faculty_seatwork_view

urlpatterns = [
    path('', faculty_seatwork_view, name='faculty_seatwork'),
]
