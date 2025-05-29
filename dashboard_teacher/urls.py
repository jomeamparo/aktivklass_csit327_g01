from django.urls import path
from .views import dashboard_view, create_class, archive_class, delete_class

urlpatterns = [
    path('', dashboard_view, name='dashboard_teacher'),
    path('create-class/', create_class, name='create_class'),
     path('class/<int:class_id>/delete/', delete_class, name='delete_class'),
    path('class/<int:class_id>/archive/', archive_class, name='archive_class'),
]
