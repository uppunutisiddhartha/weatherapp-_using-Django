from django.db import models

# Create your models here.
class Job(models.Model):
    company = models.ForeignKey( on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    required_skills = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)