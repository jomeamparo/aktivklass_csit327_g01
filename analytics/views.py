from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm


def analytics_view(request):
    context = {
        'role': 'admin'
    }
    return render(request, 'analytics/analytics.html', context)
