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
    event = get_object_or_404(Event, pk=event_id)
    polls = event.polls.order_by('pk') 
    return render(request, 'event.html', {'event': event, 'polls': polls})

def create_poll(request, event_id):
    if request.method == 'GET':
        event = get_object_or_404(Event, pk=event_id)
        return render(request, 'create-poll.html', {'event': event})
    if request.method == 'POST':
        poll_title = request.POST['poll-title']
        event = get_object_or_404(Event, pk=event_id)
        if Poll.unique_title(poll_title):
            poll = Poll(title=poll_title)
            poll.event = event
            poll.save()
            for item in request.POST['poll-categories'].split('\r\n'):
                if item:
                    category = Category(poll=poll)
                    category_info = item.split(',')
                    category.title = category_info[0]
                    if Category.unique_title(poll, category.title):
                        if len(category_info) > 1:
                            category.best_possible_rating = int(category_info[1])
                        category.save()
                    else:
                        return render(request, 'create-poll.html', {
                            'error': 'Your category names must all be unique.',
                            'event': event, 'poll_title': poll_title})
            for item in request.POST['poll-options'].split('\r\n'):
                if item:
                    option = Option(poll=poll)
                    option.title = item.split(',')[0]
                    if Option.unique_title(poll, option.title):
                        option.save()
                    else:
                        return render(request, 'create-poll.html', {
                            'error': 'Your option names must all be unique.',
                            'event': event, 'poll_title': poll_title})
            return redirect('event', event_id=event.pk)
        else:
            return render(request, 'create-poll.html', {
                'error': 'Your poll name must be unique',
                'event': event, 'poll_title': poll_title})

def view_poll(request, event_id, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    event = get_object_or_404(Event, pk=event_id)
    options = Option.objects.filter(poll=poll_id).order_by('pk') 
    categories = Category.objects.filter(poll=poll_id).order_by('pk') 
    return render(request, 'poll.html', {'event': event, 'poll': poll,
        'options': options, 'categories': categories})

