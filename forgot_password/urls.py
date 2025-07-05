from django.urls import path
# forgot_password/urls.py
from .views import forgot_password_view, reset_password_view, test_email_view

urlpatterns = [
    path('', forgot_password_view, name='forgot_password'),
    path('reset/<uuid:token>/', reset_password_view, name='reset_password'),
    # path('reset_password/', reset_password_view, name='reset_password'),  # Uncomment if you want to use this path
    path('test_email/', test_email_view, name='test_email'),
]

