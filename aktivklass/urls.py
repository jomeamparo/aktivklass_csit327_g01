from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('login.urls')),
    path('accounts/login/', RedirectView.as_view(url='/', query_string=True), name='accounts_login'),
    path('register/', include('register.urls')),
    path('dashboard_admin/', include('dashboard_admin.urls')),
    path('dashboard_teacher/', include('dashboard_teacher.urls')),
    path('dashboard_student/', include('dashboard_student.urls')),
    path('admin_faculty_list/', include('admin_faculty_list.urls')),
    path('admin_student_list/', include('admin_student_list.urls')),
    path('courses_admin/', include('courses_admin.urls')),
    path('edit_faculty/', include('edit_faculty.urls')),
    path('edit_admin/', include('edit_admin.urls')),
    path('edit_student/', include('edit_student.urls')),
    path('archived_classes/', include('archived_classes.urls')),
    path('class_join_request/', include('class_join_request.urls')),
    path('classes/', include('class_lists.urls')),
    path('class-record/', include('class_record.urls')),
    path('teacher_student/', include('teacher_student.urls')),
    path('faculty_seatwork/', include('faculty_seatwork.urls')),
    path('faculty_attendance/', include('faculty_attendance.urls')),
    path('faculty_seatworkSubmission/', include('faculty_seatworkSubmission.urls')),
    path('faculty_profile/', include('faculty_profile.urls')),
    path('faculty_settings/', include('faculty_settings.urls')),
    path('student_settings/', include('student_settings.urls')),
    path('student_profile/', include('student_profile.urls')),
    path('faculty_laboratory/', include('faculty_laboratory.urls')),
    path('notifications/', include('notifications.urls')),
    path('chat/', include('chat_screen.urls')),
    path('help_and_support/', include('help_and_support.urls')),
    path('quizzes/', include('quizzes.urls')),
    path('settings/', include('settings.urls')),
    path('analytics/', include('analytics.urls')),
    path('forgot_password/', include('forgot_password.urls')),
    path('edit_admin/', include('edit_admin.urls')),

    path('classes/', include('class_lists.urls')),
    

    path('help_and_support/', include('help_and_support.urls')),
    path('faculty_attendance/', include('faculty_attendance.urls')),
    path('attendance_student/', include('attendance_student.urls')),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='forgot_password/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='forgot_password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='forgot_password/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='forgot_password/password_reset_complete.html'), name='password_reset_complete')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
