from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .models import Notification

def faculty_notifications_dashboard(request):
    unread = Notification.objects.filter(is_read=False).order_by('-created_at')
    read = Notification.objects.filter(is_read=True).order_by('-created_at')

    return render(request, 'notifications_faculty/faculty_notifications.html', {
        'role': 'faculty',
        'new_notifications': unread,
        'old_notifications': read,
    })


def mark_as_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk)
    notification.mark_as_read()
    return redirect('faculty_notifications')

@require_POST
def mark_all_as_read(request):
    Notification.objects.filter(is_read=False).update(is_read=True)
    return redirect('faculty_notifications')