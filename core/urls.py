from django.urls import path
from . import views

urlpatterns = [
    path('test-profile/', views.test_profile, name='test_profile'),
] 