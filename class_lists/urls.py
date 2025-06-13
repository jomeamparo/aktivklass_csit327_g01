from django.urls import path
from .views import class_lists_view

urlpatterns = [
    path('', class_lists_view, name='class_lists'),
]
