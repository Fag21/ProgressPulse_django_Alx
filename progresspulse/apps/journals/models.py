from django.db import models
from django.contrib.auth.models import User

class Entry(models.Model):
    date = models.DateField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['date', 'user']
        ordering = ['-date']
        app_label = 'apps.journals'  # Add this line
    
    def __str__(self):
        return f"{self.user.username} - {self.date}"