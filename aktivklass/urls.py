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
<<<<<<< HEAD
    path('faculty_seatwork/', include('faculty_seatwork.urls')),
    path('faculty_seatworkSubmission/', include('faculty_seatworkSubmission.urls')),
=======
    path('notifications/', include('notifications.urls')),
    path('forgot_password/', include('forgot_password.urls')),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='forgot_password/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='forgot_password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='forgot_password/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='forgot_password/password_reset_complete.html'), name='password_reset_complete')
>>>>>>> 9cdd82769ea6e6c66f6e8ae9d9039182c3a0a7e1
]
