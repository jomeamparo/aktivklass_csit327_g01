# Quiz URLs have been moved to core/urls.py for global purposes
# This file is kept for any quizzes-specific URLs that may be added later

from django.urls import path
from quizzes.views import quizzes_view, update_quiz_score

urlpatterns = [
    # Quiz URLs are now handled by core app
]
