from django.shortcuts import render, redirect
'''get_object_or_404
from .models import Post, Comment'''
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def settings_view(request):
    context = {
        'role': 'admin'
    }
    return render(request, 'settings/settings.html', context) #, {'form': form})

#def save_settings(request):
    

"""def post_list(request):
    posts = Post.objects.all()
    return render(request, 'post_list.html',{'posts':posts})

def post_ detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post)
    return render(request, 'post_detail.html',{'post': post, 'comments': comments})"""