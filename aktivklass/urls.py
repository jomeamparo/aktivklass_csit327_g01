"""
URL configuration for aktivklass project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('login.urls')),
    path('register/', include('register.urls')),
    path('dashboard_admin/', include('dashboard_admin.urls')),
    path('dashboard_teacher/', include('dashboard_teacher.urls')),
    path('dashboard_student/', include('dashboard_student.urls')),
    path('admin_faculty_list/', include('admin_faculty_list.urls')),
    path('admin_student_list/', include('admin_student_list.urls')),
    path('edit_faculty/', include('edit_faculty.urls')),
    path('archived_classes/', include('archived_classes.urls')),
    path('class_join_request/', include('class_join_request.urls')),
    path('faculty_seatwork/', include('faculty_seatwork.urls')),
    path('faculty_seatworkSubmission/', include('faculty_seatworkSubmission.urls')),
    path('help_and_support/', include('help_and_support.urls')),
    path('faculty_notifications/', include('notifications_faculty.urls')),
    path('edit_admin/', include('edit_admin.urls')),
    path('classes/', include('class_lists.urls')),
    path('notifications/', include('notifications.urls'))
    path('faculty_settings/', include('faculty_settings.urls')),
    path('student_settings/', include('student_settings.urls')),

    path('student_profile/', include ('student_profile.urls')),
    path('faculty_laboratory/', include('faculty_laboratory.urls')),
    path('settings/', include('settings.urls')),
    path('analytics/', include('analytics.urls')),
    path('chat/', include('chat_screen.urls')),
    path('teacher_student/', include('teacher_student.urls')),
]
