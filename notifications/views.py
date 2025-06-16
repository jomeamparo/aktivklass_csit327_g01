from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

def notifications_view(request):
    return render(request, 'notifications/notifications.html')
# Create your views here.
