from django.shortcuts import get_object_or_404, redirect, render
from core.models import Class, Faculty
from django.contrib.auth.decorators import login_required

@login_required
def archived_classes(request):
    # Get the faculty member
    faculty = Faculty.objects.get(email=request.user.email)
    
    # Get all classes where the faculty is enrolled and is_archived is True
    classes = Class.objects.filter(
        enrollment__faculty=faculty,
        is_archived=True
    ).distinct()
    
    return render(request, 'archived_classes/archived_classes.html', {
        'classes': classes,
        'role': 'faculty'
    })

def delete_archived_class(request, class_id):
    if request.method == "POST":
        class_instance = get_object_or_404(Class, id=class_id)
        class_instance.delete()
        return redirect('archived_classes')
    return redirect('archived_classes')
