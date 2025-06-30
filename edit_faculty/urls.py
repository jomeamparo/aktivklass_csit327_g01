from django.urls import path
from . import views

urlpatterns = [
    path('edit-faculty/', views.edit_faculty_view, name='edit_faculty'),
    path('toggle-faculty-status/<str:faculty_id>/', views.toggle_faculty_status, name='toggle_faculty_status'),
]
