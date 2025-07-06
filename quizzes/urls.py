from django.urls import path
from .views import quizzes_view, update_quiz_score, delete_quiz_grade

urlpatterns = [
    path('quizzes/', quizzes_view, name='quizzes'),
    path('quiz-recordsview/', quizzes_view, name='quiz_views'),
    path('update-quiz-score/', update_quiz_score, name='update_quiz_score'),
    path('delete-quiz-grade/', delete_quiz_grade, name='delete_quiz_grade'),
]