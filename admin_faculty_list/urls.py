from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_faculty_list_view, name='admin_faculty_list'),
    path('toggle-faculty-status/<str:faculty_id>/', views.toggle_faculty_status, name='toggle_faculty_status'),
]
