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
from django.urls import include, path
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('login.urls')),
    path('register/', include('register.urls')),
    path('dashboard_teacher/', include('dashboard_teacher.urls')),
    path('dashboard_admin/', include('dashboard_admin.urls')),
    path('dashboard_student/', include('dashboard_student.urls')),
    path('admin_faculty_list/', include('admin_faculty_list.urls')),
    path('admin_student_list/', include('admin_student_list.urls')),
    path('teacher_student_list/', include('teacher_student.urls')),
    path('class_record/', include('class_record.urls')),
    path('archived_classes/', include('archived_classes.urls')),
    path('class_join_request/', include('class_join_request.urls')),
    path('notifications/', include('notifications.urls')),
    path('faculty_attendance/', include('faculty_attendance.urls')),
]
