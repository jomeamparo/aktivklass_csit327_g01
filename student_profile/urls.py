from django.urls import path
from .views import student_profile_view

urlpatterns =[
    path('', student_profile_view, name='student_profile'),
]