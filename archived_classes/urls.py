from django.urls import path
from .views import archived_classes, delete_archived_class, unarchive_class

urlpatterns = [
    path('', archived_classes, name='archived_classes'),
    path('class/<int:class_id>/delete/', delete_archived_class, name='delete_archived_class'),
    path('classes/<int:class_id>/unarchive/', unarchive_class, name='unarchive_class')
]