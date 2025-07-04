from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import (
    Class, Student, StudentProfile, Faculty, ClassJoinRequest, Enrollment, 
    ActivityRecord, Notification, Conversation, Message, AdminUser, 
    Attendance, PasswordResetToken, Post, Comment, 
    FacultyProfile, Quiz, QuizQuestion, QuizChoice, QuizAttempt, QuizResponse, QuizGrade
)

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['subject_name', 'subject_code', 'class_code', 'is_archived']
    list_filter = ['is_archived']
    search_fields = ['subject_name', 'subject_code', 'class_code']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'first_name', 'last_name', 'email', 'course', 'year', 'status']
    list_filter = ['status', 'course', 'year']
    search_fields = ['student_id', 'first_name', 'last_name', 'email']

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ['faculty_id', 'first_name', 'last_name', 'department_name', 'email', 'status']
    list_filter = ['status', 'department_name']
    search_fields = ['faculty_id', 'first_name', 'last_name', 'email']

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'class_obj', 'faculty', 'total_points', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at', 'class_obj', 'faculty']
    search_fields = ['title', 'description', 'class_obj__subject_name']
    ordering = ['-created_at']

@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'quiz', 'question_type', 'points', 'order']
    list_filter = ['question_type', 'quiz']
    search_fields = ['question_text', 'quiz__title']
    ordering = ['quiz', 'order']

@admin.register(QuizChoice)
class QuizChoiceAdmin(admin.ModelAdmin):
    list_display = ['choice_text', 'question', 'is_correct', 'order']
    list_filter = ['is_correct', 'question__quiz']
    search_fields = ['choice_text', 'question__question_text']
    ordering = ['question', 'order']

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['student', 'quiz', 'started_at', 'completed_at', 'score', 'is_completed']
    list_filter = ['is_completed', 'started_at', 'quiz']
    search_fields = ['student__first_name', 'student__last_name', 'quiz__title']
    ordering = ['-started_at']

@admin.register(QuizResponse)
class QuizResponseAdmin(admin.ModelAdmin):
    list_display = ['attempt', 'question', 'is_correct', 'points_earned']
    list_filter = ['is_correct', 'question__quiz']
    search_fields = ['attempt__student__first_name', 'question__question_text']

@admin.register(QuizGrade)
class QuizGradeAdmin(admin.ModelAdmin):
    list_display = ['student', 'quiz', 'score', 'max_score', 'percentage', 'grade_letter', 'graded_at']
    list_filter = ['grade_letter', 'graded_at', 'quiz__class_obj']
    search_fields = ['student__first_name', 'student__last_name', 'quiz__title']
    ordering = ['-graded_at']

# Register other models
admin.site.register(StudentProfile)
admin.site.register(ClassJoinRequest)
admin.site.register(Enrollment)
admin.site.register(ActivityRecord)
admin.site.register(Notification)
admin.site.register(Conversation)
admin.site.register(Message)
admin.site.register(AdminUser)
admin.site.register(Attendance)
admin.site.register(PasswordResetToken)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(FacultyProfile)
