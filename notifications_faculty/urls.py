from django.urls import path
from . import views

urlpatterns = [
    path('', views.faculty_notifications_dashboard, name='faculty_notifications'),
    path('<int:pk>/read/', views.mark_as_read, name='mark_notification_as_read'),
    path('mark-all/', views.mark_all_as_read, name='mark_all_notifications_as_read'),
    path('', views.faculty_notifications, name='faculty_notifications'),
]
