from django.db import models

class Class(models.Model):
    name = models.CharField(max_length=100)
    instructor = models.CharField(max_length=100)
    schedule = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.instructor}"
