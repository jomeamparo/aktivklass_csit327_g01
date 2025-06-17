from django.urls import path
from .views import help_and_support

urlpatterns = [
    path('', help_and_support, name='help_and_support')
]