from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.template.context_processors import csrf
import logging

from models import *

def createEvent(request):
    if request.method == 'GET':
        template = loader.get_template('create_event.html')
        context = RequestContext(request, {})
        return HttpResponse(template.render(context))
    if request.method == 'POST':
        logger = logging.getLogger('degub')
        logger.info(request.POST)
        event_title = request.POST.get('event-title', '')
        if event_title:
            event = Event(event_title)
            c = {}
            c.update(csrf(request))
            template = loader.get_template('list_events.html')
            context = RequestContext(request, c)
            return HttpResponse(template.render(context))
        else:
            template = loader.get_template('create_event.html')
            template_values = {"error_message": "Nope, didn't work"}
            context = RequestContext(request, template_values)
            return HttpResponse(template.render(context))

        

def listEvents(request):
    if request.method == 'GET':
        template = loader.get_template('list_events.html')
        context = RequestContext(request, {})
        return HttpResponse(template.render(context))