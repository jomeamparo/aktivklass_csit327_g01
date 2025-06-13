from django.urls import path
from .views import quizzes_view

urlpatterns = [
    path('', quizzes_view, name='quizzes'),
]
