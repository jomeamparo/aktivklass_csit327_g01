from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseBadRequest
from .models import Conversation, Message
from core.models import Student

def get_user_from_session(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return None
    
    try:
        return Student.objects.get(student_id=user_id)
    except Student.DoesNotExist:
        return None

def chat_home(request):
    user = get_user_from_session(request)
    if not user:
        return redirect('login')
    
    conversations = Conversation.objects.filter(participants=user).order_by('-created_at')
    return render(request, 'chat_screen/chat_home.html', {
        'conversations': conversations,
        'role': 'student'
    })

def conversation_detail(request, conversation_id):
    user = get_user_from_session(request)
    if not user:
        return redirect('login')
    
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=user)
    messages = conversation.messages.all()
    return render(request, 'chat_screen/conversation_detail.html', {
        'conversation': conversation,
        'messages': messages,
        'role': 'student'
    })

def send_message(request, conversation_id):
    user = get_user_from_session(request)
    if not user:
        return redirect('login')
    
    if request.method != 'POST':
        return HttpResponseBadRequest("Invalid request method.")

    conversation = get_object_or_404(Conversation, id=conversation_id, participants=user)
    content = request.POST.get('content', '').strip()

    if not content:
        return redirect('conversation_detail', conversation_id=conversation.id)

    Message.objects.create(
        conversation=conversation,
        sender=user,
        content=content
    )
    return redirect('conversation_detail', conversation_id=conversation.id)
