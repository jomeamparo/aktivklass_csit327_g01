from django.shortcuts import render, redirect, get_object_or_404
from core.models import AdminUser
from django.views.decorators.http import require_POST

# GET - to display the edit_admin.html with list
def edit_admin_page(request):
    admins = AdminUser.objects.all()
    return render(request, 'edit_admin.html', {'admins': admins})

# POST - for handling the save button
@require_POST
def edit_admin(request):
    admin = get_object_or_404(AdminUser, id=request.POST.get('admin_id'))
    admin.username = request.POST.get('username')
    admin.email = request.POST.get('email')
    admin.save()
    return redirect('edit_admin')

# POST - for toggling the disabled status
@require_POST
def toggle_admin_status(request, admin_id):
    admin = get_object_or_404(AdminUser, id=admin_id)
    admin.is_disabled = not admin.is_disabled  # toggle the status
    admin.save()
    return redirect('edit_admin')
