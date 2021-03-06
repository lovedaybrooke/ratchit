"""polladmin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt

import views

urlpatterns = [
    url(r"^admin/", include(admin.site.urls)),
    url(r"^$", views.list_events),
    url(r"^event/create$",  csrf_exempt(views.create_event)),
    url(r"^event/(?P<event_id>[0-9]+)/$",  views.manage_event, name="event"),
    url(r"^event/(?P<event_id>[0-9]+)/create-poll$",  csrf_exempt(views.create_poll)),
    url(r"^event/(?P<event_id>[0-9]+)/poll/(?P<poll_id>[0-9]+)$",  csrf_exempt(views.view_poll)),
    url(r"^event/(?P<event_id>[0-9]+)/poll/(?P<poll_id>[0-9]+)/results$",  views.poll_results),
    url(r'^rate', include('ratings.urls')),
]
