from django.urls import path
from . import views

app_name = "admin_notif"
 
urlpatterns = [
    path('', views.admin_notif_dashboard, name='admin_notif'),
    path('<int:pk>/read/', views.mark_as_read, name='mark_notification_as_read'),
    path('mark-all/', views.mark_all_as_read, name='mark_all_notifications_as_read'),
]
