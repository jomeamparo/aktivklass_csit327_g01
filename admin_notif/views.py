from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from core.models import Notification

def admin_notif_dashboard(request):
    notifications = Notification.objects.all().order_by('-created_at')

    return render(request, 'admin_notif/admin_notif.html', {
        'role': 'admin',
        'notifications': notifications,
    })


def mark_as_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk)
    notification.mark_as_read()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'ok'})

    return redirect('admin_notif:admin_notif')

@require_POST
def mark_all_as_read(request):
    Notification.objects.filter(is_read=False).update(is_read=True)
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'ok'})
    
    return redirect('admin_notif:admin_notif')