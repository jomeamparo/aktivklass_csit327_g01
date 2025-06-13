from django.urls import path
from .views import student_settings

urlpatterns = [
    path('', student_settings, name='student_settings'),
]


