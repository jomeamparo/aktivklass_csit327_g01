
from django.urls import path
from . import views

urlpatterns = [
    path('', views.faculty_notifications_dashboard, name='faculty_notifications'),
]