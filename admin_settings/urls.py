from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_settings_view, name='admin_settings'),
    path('save-settings/', views.save_settings, name='save_settings'),
    #path('save-settngs/', views.save_settings, name='save_settings')
    #path('post/<int:pk>/', views.post_detail, name='post_detail'),
]