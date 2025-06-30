from django.urls import path
<<<<<<< HEAD
from . import views

urlpatterns = [
    path('test-profile/', views.test_profile, name='test_profile'),
    path('records/', views.records_list, name='records_list'),
    path('api/records/', views.api_records, name='api_records'),
    path('records/export/', views.export_csv, name='export_csv'),
=======
from .views import quizzes_view, update_quiz_score

urlpatterns = [
    path('quizzes/', quizzes_view, name='quizzes'),
    path('quiz-records/', quizzes_view, name='quiz_records'),
    path('update-quiz-score/', update_quiz_score, name='update_quiz_score'),
>>>>>>> 8ee983c (feature(connected_database): fix errors in connection)
] 