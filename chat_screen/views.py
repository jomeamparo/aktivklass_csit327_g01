from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseBadRequest
from django.db.models import Q
from functools import wraps
from core.models import Conversation, Message, Student, Faculty, AdminUser
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def get_user_from_session(request):
    """Get authenticated user and role from session"""
    user_id = request.session.get('user_id')
    if not user_id:
        return None, None
    
    # Try to find user in each model
    for model, id_field in [
        (Student, 'student_id'),
        (Faculty, 'faculty_id'),
        (AdminUser, 'employee_id')
    ]:
        try:
            user = model.objects.get(**{id_field: user_id})
            role = model.__name__.lower()
            return user, role
        except model.DoesNotExist:
            continue
    
    return None, None

def student_only(view_func):
    """Decorator to restrict access to students only"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user, role = get_user_from_session(request)
        
        if not user:
            return redirect('login')
        
        if role != 'student':
            redirect_urls = {
                'faculty': 'dashboard_teacher',
                'adminuser': 'dashboard_admin'
            }
            return redirect(redirect_urls.get(role, 'login'))
        
        return view_func(request, user, *args, **kwargs)
    
    return wrapper

@student_only
def chat_home(request, user):
    """Display chat home with user's conversations"""
    conversations = _get_user_conversations(user)
    
    return render(request, 'chat_screen/chat_home.html', {
        'conversations': conversations,
        'role': 'student'
    })

@student_only
def search_students(request, user):
    """Search for students to chat with"""
    query = request.GET.get('q', '').strip()
    students = _search_students_by_query(query, user) if query else []
    
    return render(request, 'chat_screen/search_students.html', {
        'students': students,
        'query': query,
        'role': 'student'
    })

@student_only
def start_conversation(request, user, student_id):
    """Start or resume conversation with another student"""
    try:
        other_student = Student.objects.get(student_id=student_id)
        
        if other_student.id == user.id:
            return redirect('chat_home')
        
        conversation = Conversation.get_or_create_conversation(user, other_student)
        return redirect('conversation_detail', conversation_id=conversation.id)
        
    except Student.DoesNotExist:
        return redirect('chat_home')

@student_only
def conversation_detail(request, user, conversation_id):
    """Display conversation messages"""
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=user)
    other_participant = conversation.get_other_participant(user)
    
    # Mark messages as read
    _mark_messages_as_read(conversation, user)
    
    return render(request, 'chat_screen/conversation_detail.html', {
        'conversation': conversation,
        'messages': conversation.messages.all(),
        'other_participant': other_participant,
        'role': 'student'
    })

@student_only
def send_message(request, user, conversation_id):
    """Send a message in a conversation"""
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

@student_only
def mute_conversation(request, user, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=user)
    conversation.muted_by.add(user)
    messages.success(request, "Conversation muted.")
    return redirect('conversation_detail', conversation_id=conversation.id)

@student_only
def unmute_conversation(request, user, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=user)
    conversation.muted_by.remove(user)
    messages.success(request, "Conversation unmuted.")
    return redirect('conversation_detail', conversation_id=conversation.id)

# Helper functions
def _get_user_conversations(user):
    """Get user's conversations with metadata"""
    conversations = Conversation.objects.filter(participants=user).order_by('-created_at')
    
    conversation_data = []
    for conversation in conversations:
        other_participant = conversation.get_other_participant(user)
        last_message = conversation.get_last_message()
        
        conversation_data.append({
            'conversation': conversation,
            'other_participant': other_participant,
            'last_message': last_message,
            'unread_count': conversation.get_unread_count_for_user(user)
        })
    
    return conversation_data

def _search_students_by_query(query, current_user):
    """Search students by name, ID, or email"""
    return Student.objects.filter(
        Q(first_name__icontains=query) |
        Q(last_name__icontains=query) |
        Q(student_id__icontains=query) |
        Q(email__icontains=query)
    ).exclude(id=current_user.id)[:10]

def _mark_messages_as_read(conversation, user):
    """Mark unread messages as read"""
    conversation.messages.filter(
        is_read=False
    ).exclude(
        sender=user
    ).update(is_read=True)

def _get_unread_count(conversation, user):
    """Get count of unread messages for user"""
    return conversation.messages.filter(
        is_read=False
    ).exclude(
        sender=user
    ).count()
