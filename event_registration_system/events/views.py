from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import F
from .models import Event, Registration
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import EventSerializer, RegistrationSerializer
from django.http import Http404


class EventListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, event_id):
        try:
            return Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            raise Http404

    def get(self, request, event_id, format=None):
        event = self.get_object(event_id)
        serializer = EventSerializer(event)
        return Response(serializer.data)


class UserRegistrationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id, format=None):
        event = get_object_or_404(Event, pk=event_id)

        if Registration.objects.filter(user=request.user, event=event).exists():
            return Response({'detail': 'You are already registered for this event.'}, status=status.HTTP_400_BAD_REQUEST)

        if event.available_slots <= 0:
            return Response({'detail': 'No available slots for this event.'}, status=status.HTTP_400_BAD_REQUEST)

        Registration.objects.create(user=request.user, event=event)
        Event.objects.filter(pk=event_id, available_slots__gt=0).update(available_slots=F('available_slots') - 1)

        return Response({'detail': 'Registration successful.'}, status=status.HTTP_201_CREATED)


class UserRegisteredEventsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        registrations = Registration.objects.filter(user=request.user)
        serializer = RegistrationSerializer(registrations, many=True)
        return Response(serializer.data)

def homepage(request):
    return render(request, 'events/homepage.html')

@login_required
def event_list(request):
    query = request.GET.get('q')
    events = Event.objects.all()

    if query:
        events = events.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location_name__icontains=query)
        )

    return render(request, 'events/event_list.html', {'events': events, 'query': query})




@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    registration_exists = Registration.objects.filter(user=request.user, event=event).exists()
    return render(request, 'events/event_details.html', {'event': event, 'registration_exists': registration_exists})


@login_required
def register_new_event(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        date = request.POST.get('date')
        time = request.POST.get('time')
        location_name = request.POST.get('location_name')
        available_slots = request.POST.get('available_slots')

        if title and description and date and time and location_name and available_slots:
            Event.objects.create(
                title=title,
                description=description,
                date=date,
                time=time,
                location_name=location_name,
                available_slots=available_slots
            )
            messages.success(request, 'Event registered successfully.')
            return redirect('events:event_list')
        else:
            messages.error(request, 'Invalid data. Please provide all required information.')

    return render(request, 'events/register_new_event.html')


@login_required
def event_registration(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if request.method == 'POST':
        if not Registration.objects.filter(user=request.user, event=event).exists():
            if event.available_slots > 0:
                Registration.objects.create(user=request.user, event=event)
                Event.objects.filter(pk=event_id, available_slots__gt=0).update(available_slots=F('available_slots') - 1)
                return redirect('events:event_list')
            else:
                return render(request, 'events/event_registration.html', {'event': event, 'error_message': 'No available slots for this event.'})
        else:
            return render(request, 'events/event_registration.html', {'event': event, 'error_message': 'You are already registered for this event.'})

    return render(request, 'events/event_registration.html', {'event': event})


@login_required
def user_dashboard(request):
    user = request.user
    registrations = Registration.objects.filter(user=user)
    registered_events = [registration.event for registration in registrations]
    return render(request, 'events/user_dashboard.html', {'registered_events': registered_events})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. You can now log in.')
            return redirect('events:login')
    else:
        form = UserCreationForm()

    return render(request, 'events/signup.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('events:homepage')
    else:
        form = AuthenticationForm()

    return render(request, 'events/login.html', {'form': form})

@login_required
def logout_user(request):
    logout(request)
    return redirect('events:homepage')
