from django.shortcuts import render
from .models import Notification

# Create your views here.
def faculty_notifications_dashboard(request):
    # Fetch all notifications ordered by creation date
    notifications = Notification.objects.all().order_by('-created_at')
    
    return render(request, 'notifications_faculty/faculty_notifications.html', {
        'role': 'faculty',
        'notifications': notifications
    })