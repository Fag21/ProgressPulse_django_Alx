from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
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