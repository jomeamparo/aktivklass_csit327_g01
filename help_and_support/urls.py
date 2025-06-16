from django.urls import path
<<<<<<< HEAD
from .views import help_and_support

urlpatterns = [
    path('', help_and_support, name='help_and_support')
=======
from .views import help_and_support_view

urlpatterns = [
    path('', help_and_support_view, name='help_and_support'),
>>>>>>> e85a118 (feature(help_and_support): create_help_and_support_ui)
]