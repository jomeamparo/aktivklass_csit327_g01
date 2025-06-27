from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from core.models import Class

def archived_classes(request):
    classes = Class.objects.filter(is_archived=True)
    return render(request, 'archived_classes/archived_classes.html', {'classes': classes, 'role': 'faculty'})

def delete_archived_class(request, class_id):
    if request.method == "POST":
        class_instance = get_object_or_404(Class, id=class_id)
        class_instance.delete()
        return redirect('archived_classes')
    return redirect('archived_classes')

def unarchive_class(request, class_id):
    if request.method == 'POST':
        class_obj = get_object_or_404(Class, id=class_id)
        class_obj.is_archived = False
        class_obj.save()
        messages.success(request, f'Class "{class_obj.subject_name}" has been restored to active classes.')
        return redirect('archived_classes') 
    return redirect('archived_classes')