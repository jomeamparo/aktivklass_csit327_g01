from django.urls import path
from .views import dashboard_view, leave_class, join_class

urlpatterns = [
    path('', dashboard_view, name='dashboard_student'),
    path('class/<int:class_id>/leave/', leave_class, name='leave_class'),
    path('join_class/', join_class, name='join_class'),
]
