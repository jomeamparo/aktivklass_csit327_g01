from django.shortcuts import render

# Create your views here.

def faculty_notifications_view(request):
    """View for faculty notifications page"""
    return render(request, 'notifications_faculty/faculty_notifications.html')
