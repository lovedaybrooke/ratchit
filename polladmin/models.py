import os
from binascii import hexlify

from django.db import models
from django.db.models import fields


def _createHash():
    """This function generate 10 character long hash"""
    return hexlify(os.urandom(5))

class Event(models.Model):
    title = models.CharField(max_length=500, unique=True)

    @classmethod
    def unique_title(cls, test_title):
        events = Event.objects.all()
        for event_title in [event.title.lower() for event in events]:
            if event_title == test_title.lower():
                return False
        return True

class Poll(models.Model):
    event = models.ForeignKey("Event", related_name="polls")
    title = models.CharField(max_length=500, unique=True)
    rating_hash = models.CharField(max_length=10, default=_createHash,
        unique=True)

    @classmethod
    def unique_title(cls, event, title):
        if Poll.objects.filter(title=title).filter(event=event):
            return False
        else:
            return True

    @classmethod
    def create(cls, event, poll_title, option_block, category_block):
        if cls.unique_title(event, poll_title):
            poll = Poll(title=poll_title)
            poll.event = event
            poll.save()
            try:
                Category.create_from_block(poll, category_block)
                Option.create_from_block(poll, option_block)
            except NonUniqueError as e:
                raise NoneUniqueError(e)


class Option(models.Model):
    poll = models.ForeignKey("Poll", related_name="options")
    title = models.CharField(max_length=500, unique=True)

    @classmethod
    def unique_title(cls, poll, title):
        if cls.objects.filter(title=title).filter(poll=poll):
            return False
        else:
            return True

    @classmethod
    def create_from_block(cls, poll, block):
        for item in block.split('\r\n'):
            if item:
                option = cls(poll=poll)
                option.title = item.split(',')[0]
                if cls.unique_title(poll, option.title):
                    option.save()
                else:
                    raise NonUniqueError(
                        "You can't use the same option name twice")


class Category(models.Model):
    poll = models.ForeignKey("Poll", related_name="categories")
    title = models.CharField(max_length=500)
    best_possible_rating = models.IntegerField(default=3)

    @classmethod
    def unique_title(cls, poll, title):
        if cls.objects.filter(title=title).filter(poll=poll):
            return False
        else:
            return True

    @classmethod
    def create_from_block(cls, poll, block):
        for item in block.split('\r\n'):
            if item:
                item_dict = item.split(',')
                category = cls(poll=poll)
                category.title = item_dict[0].strip()
                if len(item_dict) > 1:
                        category.best_possible_rating = int(item_dict[1])
                if cls.unique_title(poll, category.title):
                    category.save()
                else:
                    raise NonUniqueError(
                        "You can't use the same category name twice.")


class NonUniqueError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
