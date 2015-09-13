from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.template.context_processors import csrf

from polladmin import models as polladmin_models
from models import *


def see_polls(request):
    polls = polladmin_models.Poll.objects.all()
    return render(request, "polls.html", {"polls": polls})


def start_poll(request, poll_hash):
    poll = polladmin_models.Poll.get_object_from_hash(poll_hash)
    category = polladmin_models.Category.get_ordered_queryset(poll)[0]
    option = polladmin_models.Option.get_ordered_queryset(poll)[0]
    request = Rater.create_if_necessary(request)
    return HttpResponseRedirect("/rate/{0}/{1}/{2}".format(poll_hash,
        option.rating_hash, category.rating_hash))


def solicit_rating(request, poll_hash, option_hash, category_hash):
    if request.method == "GET":
        poll = polladmin_models.Poll.get_object_from_hash(poll_hash)
        category = polladmin_models.Category.get_object_from_hash(poll,
            category_hash)
        option = polladmin_models.Option.get_object_from_hash(poll,
            option_hash)
        next_rating = Rating.next_rating(poll, option, category)
        return render(request, "option-category.html", {
            "poll": poll,
            "option": option,
            "category": category,
            "next_rating": next_rating,
            })


def submit_rating(request, poll_hash, option_hash, category_hash, rating):
    if request.method == "GET":
        rating = Rating(rating=rating)
        rating.poll = polladmin_models.Poll.get_object_from_hash(poll_hash)
        rating.category = polladmin_models.Category.get_object_from_hash(
            rating.poll, category_hash)
        rating.option = polladmin_models.Option.get_object_from_hash(
            rating.poll, option_hash)
        rating.rater = Rater.get_from_session(request)
        rating.save()
        return HttpResponseRedirect("/rate/{0}/{1}/{2}/next".format(poll_hash,
            option_hash, category_hash))


def confirm_rating(request, poll_hash, option_hash, category_hash):
    if request.method == "GET":
        poll = polladmin_models.Poll.get_object_from_hash(poll_hash)
        category = polladmin_models.Category.get_object_from_hash(poll,
            category_hash)
        option = polladmin_models.Option.get_object_from_hash(poll,
            option_hash)
        next_rating = Rating.next_rating(poll, option, category)
        return render(request, "option-category-confirmation.html", {
            "poll": poll,
            "option": option,
            "category": category,
            "next_rating": next_rating,
            })
