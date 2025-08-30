from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Entry

@login_required
def entry_list(request):
    entries = Entry.objects.filter(user=request.user).order_by('-date')
    return render(request, 'journals/entry_list.html', {'entries': entries})

@login_required
def entry_create(request):
    today = timezone.now().date()
    
    # Check if an entry already exists for today
    existing_entry = Entry.objects.filter(user=request.user, date=today).first()
    
    if existing_entry:
        return redirect('journals:entry_update', pk=existing_entry.pk)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Entry.objects.create(
                user=request.user,
                date=today,
                content=content
            )
            return redirect('journals:entry_list')
    
    return render(request, 'journals/entry_form.html', {'today': today})

@login_required
def entry_update(request, pk):
    entry = get_object_or_404(Entry, pk=pk, user=request.user)
    
    if request.method == 'POST':
        entry.content = request.POST.get('content')
        entry.save()
        return redirect('journals:entry_list')
    
    return render(request, 'journals/entry_form.html', {'entry': entry})

@login_required
def entry_delete(request, pk):
    entry = get_object_or_404(Entry, pk=pk, user=request.user)
    
    if request.method == 'POST':
        entry.delete()
        return redirect('journals:entry_list')
    
    return render(request, 'journals/entry_confirm_delete.html', {'entry': entry})