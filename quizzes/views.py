from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

def quizzes_view(quizzes):
    return render(quizzes, 'quizzes/quizzes.html')
