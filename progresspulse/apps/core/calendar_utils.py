import calendar
from datetime import date, timedelta
from django.utils import timezone
from apps.habits.models import DailyRecord
from apps.journals.models import Entry

def get_calendar_data(user, year=None, month=None):
    """Generate calendar data with completion information"""
    today = timezone.now().date()
    
    if not year or not month:
        year = today.year
        month = today.month
    
    # Create a calendar for the specified month
    cal = calendar.monthcalendar(year, month)
    
    # Get the first and last day of the month
    first_day = date(year, month, 1)
    if month == 12:
        last_day = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        last_day = date(year, month + 1, 1) - timedelta(days=1)
    
    # Get all habit completions for this month
    completions = DailyRecord.objects.filter(
        habit__user=user,
        date__gte=first_day,
        date__lte=last_day,
        completed=True
    ).values_list('date', flat=True)
    
    # Get all journal entries for this month
    journals = Entry.objects.filter(
        user=user,
        date__gte=first_day,
        date__lte=last_day
    ).values_list('date', flat=True)
    
    # Convert to sets for faster lookup
    completion_dates = set(completions)
    journal_dates = set(journals)
    
    # Prepare calendar data with status for each day
    calendar_data = []
    for week in cal:
        week_data = []
        for day in week:
            day_data = {'day': day, 'status': None}
            
            if day != 0:  # 0 means day doesn't belong to current month
                current_date = date(year, month, day)
                
                # Determine status based on activities
                if current_date in completion_dates and current_date in journal_dates:
                    day_data['status'] = 'both'
                elif current_date in completion_dates:
                    day_data['status'] = 'habit'
                elif current_date in journal_dates:
                    day_data['status'] = 'journal'
                elif current_date > today:
                    day_data['status'] = 'future'
            
            week_data.append(day_data)
        calendar_data.append(week_data)
    
    # Get previous and next month for navigation
    if month == 1:
        prev_year, prev_month = year - 1, 12
    else:
        prev_year, prev_month = year, month - 1
        
    if month == 12:
        next_year, next_month = year + 1, 1
    else:
        next_year, next_month = year, month + 1
    
    return {
        'calendar': calendar_data,
        'month': month,
        'month_name': calendar.month_name[month],
        'year': year,
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
        'today': today
    }