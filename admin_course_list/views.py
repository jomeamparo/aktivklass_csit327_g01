from django.shortcuts import redirect, render
from django.urls import reverse
from core.models import Course
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db import connection

def admin_course_list_view(request):
    if request.method == "POST":
        action = request.POST.get("action", "add")  # Default to add if not specified
        course_id = request.POST.get("course_id")
        subject_name = request.POST.get("subject_name")
        subject_code = request.POST.get("subject_code")
        section = request.POST.get("section")
        schedule = request.POST.get("schedule")
        capacity = request.POST.get("capacity")
        room = request.POST.get("room")

        if all([course_id, subject_name, subject_code, section, schedule, capacity, room]):
            if action == "edit":
                # Update existing course
                try:
                    course = Course.objects.get(course_id=course_id)
                    course.subject_name = subject_name
                    course.subject_code = subject_code
                    course.section = section
                    course.schedule = schedule
                    course.capacity = capacity
                    course.room = room
                    course.save()
                except Course.DoesNotExist:
                    pass  # Handle error if needed
            else:
                # Add new course
                if not Course.objects.filter(course_id=course_id).exists():
                    Course.objects.create(
                        course_id=course_id,
                        subject_name=subject_name,
                        subject_code=subject_code,
                        section=section,
                        schedule=schedule,
                        capacity=capacity,
                        room=room,
                    )

        return redirect(reverse('admin_course_list'))

    courseList = Course.objects.all().order_by('course_id')
    context = {
        'courseList': courseList,
        'role': 'admin'
    }
    return render(request, 'admin_course_list/course_list.html', context)