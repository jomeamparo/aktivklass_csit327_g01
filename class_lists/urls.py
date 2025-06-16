# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('classes/', views.class_list_view, name='class_list'),
    path('classes/<int:class_id>/', views.class_detail_view, name='class_detail'),
    path('classes/<int:class_id>/join/', views.join_class_view, name='join_class'),
]
