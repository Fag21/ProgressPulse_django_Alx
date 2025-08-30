from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.habits.models import Habit
from apps.journals.models import Entry
from django.utils import timezone

def home(request):
    return render(request, 'core/home.html')

@login_required
def dashboard(request):
    today = timezone.now().date()
    
    # Get today's habits
    habits = Habit.objects.filter(user=request.user)
    
    # Check if user has a journal entry for today
    todays_entry = Entry.objects.filter(user=request.user, date=today).first()
    
    context = {
        'habits': habits,
        'todays_entry': todays_entry,
        'today': today,
    }
    
    return render(request, 'core/dashboard.html', context)