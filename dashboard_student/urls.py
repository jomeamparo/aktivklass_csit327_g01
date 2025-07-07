from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard_student'),
    path('leave-class/<int:class_id>/', views.leave_class, name='leave_class'),
    path('join-class/', views.join_class, name='join_class'),
    path('toggle-archive/<int:enrollment_id>/', views.toggle_archive_view, name='toggle_archive'),
]
