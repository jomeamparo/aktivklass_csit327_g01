from django.urls import path
from .views import help_and_support_view

urlpatterns = [
    path('', help_and_support_view, name='help_and_support'),
]