from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_home, name='chat_home'),
    path('search/', views.search_students, name='search_students'),
    path('start/<str:student_id>/', views.start_conversation, name='start_conversation'),
    path('conversation/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    path('conversation/<int:conversation_id>/send/', views.send_message, name='send_message'),
    path('conversation/<int:conversation_id>/mute/', views.mute_conversation, name='mute_conversation'),
    path('conversation/<int:conversation_id>/unmute/', views.unmute_conversation, name='unmute_conversation'),
]
