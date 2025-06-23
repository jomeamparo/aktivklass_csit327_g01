from django.urls import path
from . import views

urlpatterns = [
    path('help_and_support/', views.help_and_support, name='help_and_support'),
]