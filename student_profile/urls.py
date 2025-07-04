from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_profile_view, name='student_profile'),
    path('update_status/<str:student_id>/', views.update_student_status, name='update_student_status'),
    path('search/', views.search_student_profiles, name='search_student_profiles'),
    path('<str:student_id>/', views.view_student_profile, name='view_student_profile'),
]