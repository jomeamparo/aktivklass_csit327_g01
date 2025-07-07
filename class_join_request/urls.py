from django.urls import path
from .views import class_join_request_view, approve_join_request, reject_join_request, debug_join_requests

urlpatterns = [
    path('', class_join_request_view, name='class_join_request'),
    path('debug/', debug_join_requests, name='debug_join_requests'),
    path('join-request/<int:request_id>/approve/', approve_join_request, name='approve_join_request'),
    path('join-request/<int:request_id>/reject/', reject_join_request, name='reject_join_request'),
]
