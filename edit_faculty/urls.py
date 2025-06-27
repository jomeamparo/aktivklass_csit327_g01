from django.urls import path
from . import views

app_name = 'edit_faculty'

urlpatterns = [
    path('', views.faculty_list_view, name='faculty_list'),
    path('<str:faculty_id>/', views.edit_faculty_view, name='edit_faculty_view'),
    path('update/<str:faculty_id>/', views.update_faculty, name='update_faculty'),
]