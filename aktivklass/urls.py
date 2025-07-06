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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('login.urls')),
    path('accounts/login/', RedirectView.as_view(url='/', query_string=True), name='accounts_login'),
    path('register/', include('register.urls')),
    path('dashboard_teacher/', include('dashboard_teacher.urls')),
    path('dashboard_admin/', include('dashboard_admin.urls')),
    path('dashboard_student/', include('dashboard_student.urls')),
    path('admin_faculty_list/', include('admin_faculty_list.urls')),
    path('admin_student_list/', include('admin_student_list.urls')),
    path('edit_faculty/', include('edit_faculty.urls')),
    path('edit_student/', include('edit_student.urls')),
    path('teacher_student/', include('teacher_student.urls')),
    path('archived_classes/', include('archived_classes.urls')),
    path('class_join_request/', include('class_join_request.urls')),
    path('faculty_seatwork/', include('faculty_seatwork.urls')),
    path('faculty_attendance/', include('faculty_attendance.urls')),
    path('faculty_profile/', include('faculty_profile.urls')),
    path('faculty_settings/', include('faculty_settings.urls')),
    path('student_settings/', include('student_settings.urls')),
    path('student_profile/', include('student_profile.urls')),
    path('faculty_laboratory/', include('faculty_laboratory.urls')),
    path('notifications/', include('notifications.urls')),
    path('faculty_notifications/', include('notifications_faculty.urls')),
    path('chat/', include('chat_screen.urls')),
    path('help_and_support/', include('help_and_support.urls')),
    path('', include('core.urls')),
    path('admin_settings/', include('admin_settings.urls')),
    path('analytics/', include('analytics.urls')),
    path('forgot_password/', include('forgot_password.urls')),
    path('admin_notif/', include(('admin_notif.urls', 'admin_notif'), namespace='admin_notif')),
    path('admin_course_list/', include('admin_course_list.urls')),
    path('faculty_notifications/', include('notifications_faculty.urls')),
    path('help_and_support/', include('help_and_support.urls')),
    path('attendance_student/', include('attendance_student.urls')),
    path('core/', include('core.urls')),
    path('class_lists/', include('class_lists.urls')),
    path('class_record/', include('class_record.urls')), 
    path('quizzes/', include('quizzes.urls')),

    
    # Password reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='forgot_password/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='forgot_password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='forgot_password/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='forgot_password/password_reset_complete.html'), name='password_reset_complete')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
