import os
from binascii import hexlify
import logging

from django.db import models
from django.db.models import fields

from polladmin.models import Option, Category, Poll


def _createHash():
    """This function generate 10 character long hash"""
    return hexlify(os.urandom(5))


class Rater(models.Model):
    id_hash = models.CharField(max_length=10, default=_createHash,
        unique=True)

    @classmethod
    def create_if_necessary(cls, request):
        if 'rater' not in request.session:
            new_rater = cls()
            new_rater.save()
            request.session['rater'] = new_rater.id_hash
        return request

    @classmethod
    def get_from_session(cls, request):
        return cls.objects.filter(id_hash=request.session['rater']).get()


class Rating(models.Model):
    poll = models.ForeignKey(Poll, related_name="ratings")
    option = models.ForeignKey(Option, related_name="ratings")
    category = models.ForeignKey(Category, related_name="ratings")
    rater = models.ForeignKey("Rater", related_name="ratings")
    rating = models.IntegerField()

    @classmethod
    def next_rating(cls, poll, previous_option, previous_category):
        all_options = list(Option.objects.filter(poll=poll).order_by('id'
            ).all())
        all_categories = list(Category.objects.filter(poll=poll).order_by(
            'id').all())
        previous_category_position = all_categories.index(previous_category)
        previous_option_position = all_options.index(previous_option)
        if previous_category_position < (len(all_categories) - 1):
            new_category = all_categories[previous_category_position + 1]
            new_option = previous_option
        else:
            if previous_option_position < (len(all_options) - 1):
                new_category = all_categories[0]
                new_option = all_options[previous_option_position + 1]
            else:
                return False
        return {"option_hash": new_option.rating_hash,
            "category_hash": new_category.rating_hash}

    def set_numerical_rating(self, rating_word):
        if rating_word == "middle":
            self.rating = 2
        if rating_word == "most":
            self.rating = self.category.best_possible_rating
        if rating_word == "least":
            self.rating = self.category.best_possible_rating * -1 + 4


