from django.urls import path
from .views import laboratory_view, dashboard

urlpatterns = [
    path('', laboratory_view, name='faculty_laboratory'),
    path('dashboard/', dashboard, name='dashboard'),  
]
