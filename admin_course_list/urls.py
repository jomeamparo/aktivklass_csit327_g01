from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_course_list_view, name='admin_course_list'),
]