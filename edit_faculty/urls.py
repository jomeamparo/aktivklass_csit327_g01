from django.urls import path
from .views import edit_faculty_view

urlpatterns = [
    path('', edit_faculty_view, name='edit_faculty')
]