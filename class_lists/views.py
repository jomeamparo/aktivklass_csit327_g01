from django.shortcuts import render, get_object_or_404, redirect
from .models import Class, Enrollment
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def class_list_view(request):
    classes = Class.objects.all()
    return render(request, 'class_lists/class_list.html', {'classes': classes})

@login_required
def class_detail_view(request, class_id):
    selected_class = get_object_or_404(Class, id=class_id)
    return render(request, 'class_lists/class_detail.html', {'class': selected_class})

@login_required
def join_class_view(request, class_id):
    selected_class = get_object_or_404(Class, id=class_id)
    student = request.user

    # Prevent duplicate enrollments
    if Enrollment.objects.filter(student=student, enrolled_class=selected_class).exists():
        messages.warning(request, "You have already joined this class.")
    else:
        Enrollment.objects.create(student=student, enrolled_class=selected_class)
        messages.success(request, "Successfully joined the class.")

    return redirect('class_detail', class_id=class_id)
