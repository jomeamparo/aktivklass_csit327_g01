from django.db import models

class Post(models.Model):

    title = models.CharField(max_length=100)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)

    def str (self):
        return self.title

class Comment(models.Model):
    post = models. ForeignKey (Post, on_delete=models.CASCADE)
    text = models.TextField()
    author = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def str (self):
        return f'(self.author) on (self.post.title)'

class AdminUser(models.Model):
    username = models.CharField(max_length=150)
    email = models.EmailField()
    is_disabled = models.BooleanField(default=False)

    def __str__(self):
        return self.username