from django.urls import path
from .views import student_profile_view, update_student_status

urlpatterns =[
    path('', student_profile_view, name='student_profile'),
    path('update_status/<str:student_id>/', update_student_status, name='update_student_status'),
]