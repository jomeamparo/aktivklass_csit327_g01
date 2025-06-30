from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

def faculty_seatwork_view(request):
    context =  {
        'role': 'faculty'
    }
    return render(request, 'faculty_seatwork/faculty_seatwork.html', context)
