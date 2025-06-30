from django.urls import path
from . import views
from quizzes.views import quizzes_view, update_quiz_score

urlpatterns = [
    path('test-profile/', views.test_profile, name='test_profile'),
    path('records/', views.records_list, name='records_list'),
    path('api/records/', views.api_records, name='api_records'),
    path('records/export/', views.export_csv, name='export_csv'),
    path('quizzes/', quizzes_view, name='quizzes'),
    path('quiz-recordsview/', quizzes_view, name='quiz_views'),
    path('update-quiz-score/', update_quiz_score, name='update_quiz_score'),
] 