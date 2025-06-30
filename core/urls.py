from django.urls import path
from quizzes.views import quizzes_view, update_quiz_score

urlpatterns = [
    path('quizzes/', quizzes_view, name='quizzes'),
    path('quiz-recordsview/', quizzes_view, name='quiz_views'),
    path('update-quiz-score/', update_quiz_score, name='update_quiz_score'),
] 