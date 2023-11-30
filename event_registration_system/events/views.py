from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import F
from .models import Event, Registration

def event_list(request):
    events = Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events})

def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'events/event_detail.html', {'event': event})

@login_required
def event_registration(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if request.method == 'POST':
        # Check if the user is already registered for the event
        if not Registration.objects.filter(user=request.user, event=event).exists():
            # Check if there are available slots
            if event.available_slots > 0:
                # Register the user for the event
                Registration.objects.create(user=request.user, event=event)
                # Decrement the available slots
                Event.objects.filter(pk=event_id, available_slots__gt=0).update(available_slots=F('available_slots') - 1)
                return redirect('event_list')
            else:
                return render(request, 'events/event_registration.html', {'event': event, 'error_message': 'No available slots for this event.'})
        else:
            return render(request, 'events/event_registration.html', {'event': event, 'error_message': 'You are already registered for this event.'})

    return render(request, 'events/event_registration.html', {'event': event})

@login_required
def user_dashboard(request):
    registrations = Registration.objects.filter(user=request.user)
    return render(request, 'events/user_dashboard.html', {'registrations': registrations})
