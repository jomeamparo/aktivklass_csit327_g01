# urls.py

from django.urls import path
from .views import class_list_view, join_class_view

urlpatterns = [
    path('', class_list_view, name='class_list'),
    path('join/<int:class_id>/', join_class_view, name='join_class_view'),
]
