from django.urls import path
from .views import login_view, logout_view, forgot_password

urlpatterns = [
    path('', login_view, name='login'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('logout/', logout_view, name='logout'),
]
