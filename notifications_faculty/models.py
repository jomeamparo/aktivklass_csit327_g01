from django.db import models

# Create your models here.
class Notification(models.Model):
    title = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def mark_as_read(self):
        self.is_read = True
        self.save()

    def __str__(self):
        return '{self.title}'
    
# create a test notification in the shell like this
# Notification.objects.create(
#     title="New Message",
#     message="You have received a new message."
# )