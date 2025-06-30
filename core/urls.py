from django.urls import path
from .views import quizzes_view, update_quiz_score

urlpatterns = [
    path('quizzes/', quizzes_view, name='quizzes'),
    path('quiz-records/', quizzes_view, name='quiz_records'),
    path('update-quiz-score/', update_quiz_score, name='update_quiz_score'),
] 