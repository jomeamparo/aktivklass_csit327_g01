from django.shortcuts import render, redirect
'''get_object_or_404
from .models import Post, Comment'''
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def admin_settings_view(request):
    context = {
        'role': 'admin'
    }
    return render(request, 'settings/settings.html', context) #, {'form': form})

def save_settings(request):
    if request.method == "POST" and request.headers.get("Content-Type") == "application/json":
        try:
            data = json.loads(request.body)
            theme = data.get("theme")
            language = data.get("language")
            notifications = data.get("notifications")

            print("Saved settings:", data)

            # Optional: Save to session, DB, etc.            
            request.session['theme'] = theme
            request.session['language'] = language
            request.session['notifications'] = notifications

            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "Invalid request"})
    

"""def post_list(request):
    posts = Post.objects.all()
    return render(request, 'post_list.html',{'posts':posts})

def post_ detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post)
    return render(request, 'post_detail.html',{'post': post, 'comments': comments})"""