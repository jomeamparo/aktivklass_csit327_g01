from django.urls import path
from .views import laboratory_view

urlpatterns = [

    path('', laboratory_view, name='faculty_laboratory'),
    path('faculty_laboratory/', laboratory_view, name='faculty_laboratory'),
]
