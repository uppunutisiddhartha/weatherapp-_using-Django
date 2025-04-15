

# Create your models here.
from django.db import models

class Suggestion(models.Model):
    email = models.EmailField()
    title = models.CharField(max_length=255)
    suggestion = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.email})"
