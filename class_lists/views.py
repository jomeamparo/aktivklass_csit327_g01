from django.shortcuts import render
from .models import Class

def class_lists_view(request):
    classes = Class.objects.all()
    return render(request, 'class_lists/class_lists.html', {'classes': classes})
