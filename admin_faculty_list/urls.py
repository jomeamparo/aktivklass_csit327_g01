from django.urls import path
from .views import admin_faculty_list_view

urlpatterns = [
    path('', admin_faculty_list_view, name='faculty_list_view'),
    
]
