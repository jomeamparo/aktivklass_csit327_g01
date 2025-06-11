from django.urls import path
# forgot_password/urls.py
from .views import forgot_password_view

urlpatterns = [
    path('', forgot_password_view, name='forgot_password'),
]
