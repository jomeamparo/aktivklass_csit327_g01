from django.urls import path
from . import views

urlpatterns = [
    path('test-profile/', views.test_profile, name='test_profile'),
    path('records/', views.records_list, name='records_list'),
    path('api/records/', views.api_records, name='api_records'),
    path('records/export/', views.export_csv, name='export_csv'),
]