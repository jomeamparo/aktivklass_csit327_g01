from django.urls import path
from . import views  # ✅ make sure you import views

urlpatterns = [
    path('', views.class_list_view, name='class_list'),
    path('join/<int:class_id>/', views.join_class_view, name='join_class_view'),
    path('archive/<int:class_id>/', views.archive_class_view, name='archive_class'),  # ✅ Add this here
]
