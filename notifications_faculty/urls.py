from django.urls import path
from . import views

urlpatterns = [
    path('', views.faculty_notifications_view, name='faculty_notifications'),
]
