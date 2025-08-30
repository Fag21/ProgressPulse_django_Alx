from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.habits.models import Habit, DailyRecord
from apps.journals.models import Entry
from django.utils import timezone
from .calendar_utils import get_calendar_data
from .quotes import get_daily_quote

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
    
    # Get calendar data for the current month
    calendar_data = get_calendar_data(request.user)
    
    # Get daily inspirational quote
    daily_quote = get_daily_quote()
    
    context = {
        'habits': habits,
        'todays_entry': todays_entry,
        'today': today,
        'completion_percentage': completion_percentage,
        'completed_habits': completed_habits,
        'total_habits': total_habits,
        'calendar_data': calendar_data,
        'daily_quote': daily_quote,
    }
    
    return render(request, 'core/dashboard.html', context)

# Add this missing function
@login_required
def calendar_view(request, year=None, month=None):
    """Display a calendar with progress tracking"""
    calendar_data = get_calendar_data(request.user, year, month)
    return render(request, 'core/calendar.html', calendar_data)