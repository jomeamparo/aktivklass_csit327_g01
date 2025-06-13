from django.db import models

# Create your models here.
'''class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    borrowed_by = models.CharField(max_length=100, blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title'''

"""class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    author = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f'{self.author} on {self.post.title}'"""