from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.context_processors import csrf
import logging

from models import *


def create_event(request):
    if request.method == "POST":
        event_title = request.POST["event-title"]
        try:
            event = Event(title=event_title)
            event.save()
            return redirect("event", event_id=event.pk)
        except:
            return render(request, "list_events.html", {
                "error": "That event name has already been taken. "
                "Please choose another.",
                "events": Event.objects.order_by("-title")})


def list_events(request):
    if request.method == "GET":
        events = Event.objects.order_by("-title")
        return render(request, "list_events.html", {"events": events})


def manage_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    polls = event.polls.order_by("pk")
    return render(request, "event.html", {"event": event, "polls": polls})


def create_poll(request, event_id):
    if request.method == "GET":
        event = get_object_or_404(Event, pk=event_id)
        return render(request, "create-poll.html", {"event": event})
    if request.method == "POST":
        try:
            event = get_object_or_404(Event, pk=event_id)
            Poll.create(event, request.POST["poll-title"],
                request.POST["poll-options"], request.POST["poll-categories"])
            return redirect("event", event_id=event.pk)
        except NonUniqueError as e:
            return render(request, "create-poll.html",
                {"error": e,
                "event": event,
                "poll_title": poll_title})


def view_poll(request, event_id, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    event = get_object_or_404(Event, pk=event_id)
    options = Option.objects.filter(poll=poll_id).order_by("pk")
    categories = Category.objects.filter(poll=poll_id).order_by("pk")
    return render(request, "poll.html", {"event": event, "poll": poll,
        "options": options, "categories": categories})
