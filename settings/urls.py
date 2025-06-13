from django.urls import path
from .views import settings_view

urlpatterns = [
    path('', settings_view, name='settings'),
    #path('save-settngs/', views.save_settings, name='save_settings')
    #path('post/<int:pk>/', views.post_detail, name='post_detail'),
]