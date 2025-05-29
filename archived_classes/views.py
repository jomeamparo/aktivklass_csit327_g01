from django.shortcuts import get_object_or_404, redirect, render

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
