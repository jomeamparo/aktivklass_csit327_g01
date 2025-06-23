from django.shortcuts import render
from core.models import Student, Faculty, AdminUser

# Create your views here.

def user_context_processor(request):
    """
    Context processor to add user information to all templates.
    This ensures the sidebar shows the correct email for the logged-in user.
    """
    context = {'avatar_url': None}
    
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        
        # Try to get the user from Student model
        student = Student.objects.filter(student_id=user_id).first()
        if student:
            context['fullname'] = f"{student.first_name} {student.last_name}"
            context['email'] = student.email
            context['role'] = 'student'
            if hasattr(student, 'profile') and student.profile.avatar:
                context['avatar_url'] = student.profile.avatar.url
            return context
            
        # Try to get the user from Faculty model
        faculty = Faculty.objects.filter(faculty_id=user_id).first()
        if faculty:
            context['fullname'] = f"{faculty.first_name} {faculty.last_name}"
            context['email'] = faculty.email
            context['role'] = 'faculty'
            return context
            
        # Try to get the user from AdminUser model
        admin = AdminUser.objects.filter(employee_id=user_id).first()
        if admin:
            context['fullname'] = f"{admin.first_name} {admin.last_name}"
            context['email'] = admin.email
            context['role'] = 'admin'
            return context
    
    # Default values if no user is found or not logged in
    context['fullname'] = "Guest User"
    context['email'] = ""
    context['role'] = 'guest'
    
    return context
