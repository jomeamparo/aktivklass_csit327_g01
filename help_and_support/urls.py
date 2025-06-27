from django.urls import path
<<<<<<< HEAD
from . import views

urlpatterns = [
    path('help_and_support/', views.help_and_support, name='help_and_support'),
] 
=======
from .views import help_and_support_view

urlpatterns = [
    path('', help_and_support_view, name='help_and_support'),
]
>>>>>>> 66dec5a (feature(help&supp.fac): new changes)
