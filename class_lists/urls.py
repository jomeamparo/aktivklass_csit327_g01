# urls.py

from django.urls import path
from .views import class_list_view, class_detail_view, join_class_view, pending_requests_view, toggle_favorite_view

urlpatterns = [
    path('', class_list_view, name='class_list'),
    path('detail/<int:class_id>/', class_detail_view, name='class_record_detail'),
    path('join/<int:class_id>/', join_class_view, name='join_class_view'),
    path('pending-requests/', pending_requests_view, name='pending_requests'),
    path('toggle-fav/<int:class_id>/', toggle_favorite_view, name='toggle_favorite'),
]