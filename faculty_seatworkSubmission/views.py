from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm


def faculty_seatworkSubmission_views(request):
    return render(request, 'faculty_seatworkSubmission/faculty_seatworkSubmission.html')
