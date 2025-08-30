from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.habits.models import Habit, DailyRecord
from apps.journals.models import Entry
from django.utils import timezone



def home(request):
    return render(request, 'core/home.html')

@login_required
def dashboard(request):
    today = timezone.now().date()
    
    # Get today's habits with completion status
    habits = Habit.objects.filter(user=request.user)
    for habit in habits:
        habit.completed_today = DailyRecord.objects.filter(
            habit=habit, 
            date=today, 
            completed=True
        ).exists()
    
    # Calculate completion percentage
    total_habits = habits.count()
    completed_habits = sum(1 for habit in habits if habit.completed_today)
    completion_percentage = (completed_habits / total_habits * 100) if total_habits > 0 else 0
    
    # Check if user has a journal entry for today
    todays_entry = Entry.objects.filter(user=request.user, date=today).first()
    
    context = {
        'habits': habits,
        'todays_entry': todays_entry,
        'today': today,
        'completion_percentage': completion_percentage,
        'completed_habits': completed_habits,
        'total_habits': total_habits,
    }
    
    return render(request, 'core/dashboard.html', context)