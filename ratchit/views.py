from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.context_processors import csrf
import logging

from models import *

def create_event(request):
    if request.method == 'POST':
        event_title = request.POST['event-title']
        try:
            event = Event(title=event_title)
            event.save()
            return redirect('event', event_id=event.pk)
        except:
            return render(request, 'list_events.html', {
                'error': 'That name has already been taken. Please choose another.',
                'events': Event.objects.order_by('-title')})

def list_events(request):
    if request.method == 'GET':
        events = Event.objects.order_by('-title') 
        return render(request, 'list_events.html', {'events': events})

def manage_event(request, event_id):
    # event = get_object_or_404(Event, pk=event_id)
    event = Event.objects.get(pk=event_id)
    return render(request, 'event.html', {'event': event})
