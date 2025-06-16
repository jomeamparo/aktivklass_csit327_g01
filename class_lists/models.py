from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(default="No description")

    def __str__(self):
        return self.title

class Class(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    section = models.CharField(max_length=20)
    schedule = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.subject.title} - {self.section}"

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    enrolled_class = models.ForeignKey(Class, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('student', 'enrolled_class')
