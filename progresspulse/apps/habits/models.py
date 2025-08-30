from django.db import models
from django.contrib.auth.models import User

class Habit(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        app_label = 'apps.habits'  # Add this line
    
    def __str__(self):
        return self.name

class DailyRecord(models.Model):
    date = models.DateField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='records')
    
    class Meta:
        unique_together = ['date', 'habit']
        app_label = 'apps.habits'  # Add this line
    
    def __str__(self):
        return f"{self.habit.name} - {self.date}"