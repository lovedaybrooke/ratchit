from django.conf.urls import include, url
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt

import views

urlpatterns = [
    url(r'^$', views.see_polls),
    url(r"^/(?P<poll_hash>[0-9a-z]+)$", views.start_poll),
    url(r"^/(?P<poll_hash>[0-9a-z]+)/(?P<option_hash>[0-9a-z]+)/(?P<category_hash>[0-9a-z]+)$", views.solicit_rating),
    url(r"^/(?P<poll_hash>[0-9a-z]+)/(?P<option_hash>[0-9a-z]+)/(?P<category_hash>[0-9a-z]+)/(?P<rating_word>(most|middle|least))$", views.submit_rating),
    url(r"^/(?P<poll_hash>[0-9a-z]+)/(?P<option_hash>[0-9a-z]+)/(?P<category_hash>[0-9a-z]+)/next$", views.confirm_rating),
]
