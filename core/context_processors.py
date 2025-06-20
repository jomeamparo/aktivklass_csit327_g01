from core.models import FacultyProfile

def faculty_profile(request):
    if request.user.is_authenticated:
        profile = FacultyProfile.objects.first()  # Adjust if you have user linkage
        return {'faculty': profile}
    return {} 