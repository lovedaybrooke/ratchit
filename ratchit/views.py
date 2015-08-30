from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
import logging

from models import *

def createEvent(request):
    if request.method == 'GET':
        template = loader.get_template('create_event.html')
        context = RequestContext(request, {})
        return HttpResponse(template.render(context))

def listEvents(request):
    if request.method == 'GET':
        template = loader.get_template('list_events.html')
        context = RequestContext(request, {})
        return HttpResponse(template.render(context))