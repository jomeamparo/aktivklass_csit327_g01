from django.urls import path
from . import views 



urlpatterns = [
    path('', views.faculty_settings_view, name='faculty_settings'),
   
]
