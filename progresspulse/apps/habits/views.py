from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Habit, DailyRecord

@login_required
def habit_list(request):
    habits = Habit.objects.filter(user=request.user)
    return render(request, 'habits/habit_list.html', {'habits': habits})

@login_required
def habit_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        if name:
            Habit.objects.create(user=request.user, name=name, description=description)
            return redirect('habits:habit_list')
    return render(request, 'habits/habit_form.html')

@login_required
def habit_update(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    if request.method == 'POST':
        habit.name = request.POST.get('name')
        habit.description = request.POST.get('description', '')
        habit.save()
        return redirect('habits:habit_list')
    return render(request, 'habits/habit_form.html', {'habit': habit})

@login_required
def habit_delete(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    if request.method == 'POST':
        habit.delete()
        return redirect('habits:habit_list')
    return render(request, 'habits/habit_confirm_delete.html', {'habit': habit})


@login_required
def habit_list(request):
    habits = Habit.objects.filter(user=request.user)
    today = timezone.now().date()
    
    # Check completion status for each habit today
    for habit in habits:
        habit.completed_today = DailyRecord.objects.filter(
            habit=habit, 
            date=today, 
            completed=True
        ).exists()
    
    return render(request, 'habits/habit_list.html', {
        'habits': habits,
        'today': today
    })

@login_required
def toggle_habit_completion(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    today = timezone.now().date()
    
    # Check if a record already exists for today
    record, created = DailyRecord.objects.get_or_create(
        habit=habit,
        date=today,
        defaults={'completed': True}
    )
    
    # If it already exists, toggle the completion status
    if not created:
        record.completed = not record.completed
        record.save()
    
    # Redirect back to the previous page
    redirect_url = request.META.get('HTTP_REFERER', 'habits:habit_list')
    return redirect(redirect_url)