from django.urls import path
from . import views  # ✅ This line is required

urlpatterns = [
    path('edit_admin', views.edit_admin_page, name='edit_admin'),  # GET
    path('edit_admin/', views.edit_admin, name='edit_admin'),  # POST
    path('toggle-admin/<int:admin_id>/', views.toggle_admin_status, name='toggle_admin_status'),  # POST
]
