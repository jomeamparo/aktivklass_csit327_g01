from django.db import ProgrammingError
from faculty_profile.views import MockFacultyProfile
from core.models import FacultyProfile

def user_context_processor(request):
    """
    Context processor to add user information to all templates.
    This ensures the sidebar shows the correct user info (Student, Faculty, Admin).
    """
    context = {
        'fullname': "Guest User",
        'email': "",
        'role': 'guest',
        'avatar_url': None
    }

    # The user role and ID should be stored in the session upon login.
    # e.g., request.session['role'] = 'faculty'
    # e.g., request.session['user_id'] = faculty.faculty_id
    
    role = request.session.get('role')
    user_id = request.session.get('user_id')

    # If we have mock profile data, use it regardless of role/user_id
    if 'mock_profile' in request.session:
        mock_profile_data = request.session['mock_profile']
        context.update({
            'fullname': f"{mock_profile_data.get('first_name', '')} {mock_profile_data.get('last_name', '')}",
            'email': mock_profile_data.get('email', ''),
            'role': 'faculty',
            'avatar_url': mock_profile_data.get('profile_picture_url')
        })
        return context

    if not role or not user_id:
        return context

    try:
        if role == 'student':
            from core.models import Student
            user = Student.objects.select_related('profile').filter(student_id=user_id).first()
            if user:
                context.update({
                    'fullname': f"{user.first_name} {user.last_name}",
                    'email': user.email,
                    'role': 'student',
                    'avatar_url': user.profile.avatar.url if hasattr(user, 'profile') and user.profile.avatar else None
                })
        elif role == 'admin':
            from core.models import AdminUser
            user = AdminUser.objects.filter(employee_id=user_id).first()
            if user:
                context.update({
                    'fullname': f"{user.first_name} {user.last_name}",
                    'email': user.email,
                    'role': 'admin',
                })
        elif role == 'faculty':
            # This is where we handle the faculty case, including the mock profile
            try:
                from core.models import Faculty
                user = Faculty.objects.filter(faculty_id=user_id).first()
                if user:
                    context.update({
                        'fullname': f"{user.first_name} {user.last_name}",
                        'email': user.email,
                        'role': 'faculty',
                        # 'avatar_url': user.facultyprofile.profile_picture.url if hasattr(user, 'facultyprofile') and user.facultyprofile.profile_picture else None
                    })
            except (ProgrammingError, AttributeError):
                # If database table doesn't exist, use default faculty info
                context.update({
                    'fullname': f"Faculty User",
                    'email': f"{user_id}@cit.edu",
                    'role': 'faculty',
                })
    except ProgrammingError:
        # This is a fallback for other roles if their tables don't exist yet.
        pass

    return context 

def user_profile_context(request):
    profile = None
    if request.user.is_authenticated:
        try:
            profile = FacultyProfile.objects.get(user=request.user)
        except FacultyProfile.DoesNotExist:
            profile = None
    elif 'mock_profile' in request.session:
        # For mock mode, use a simple object for template compatibility
        class SessionProfile:
            pass
        profile = SessionProfile()
        for k, v in request.session['mock_profile'].items():
            setattr(profile, k, v)
    return {'sidebar_profile': profile} 