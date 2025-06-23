from django.urls import path
from . import views

urlpatterns = [
    path('help-and-support/', views.help_and_support, name='help_and_support'),
] 