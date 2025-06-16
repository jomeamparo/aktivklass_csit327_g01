<<<<<<< HEAD
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
 
 
def notifications_view(request):
    return render(request, 'notifications/notifications.html')
=======
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

def notifications_view(request):
    return render(request, 'notifications/notifications.html')
# Create your views here.
>>>>>>> de8d8cd (feature(notification): create_notification_screen_UI)
