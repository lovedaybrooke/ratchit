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
    def unique_title(cls, event, test_title):
        polls = cls.objects.filter(event=event)
        for poll_title in [poll.title.lower() for poll in polls]:
            if poll_title == test_title.lower():
                return False
        return True

    @classmethod
    def create(cls, event, poll_title, option_block, category_block_desc,
        category_block_asc):
        if cls.unique_title(event, poll_title):
            poll = cls(title=poll_title)
            poll.event = event
            poll.save()
            Category.create_from_blocks(poll, category_block_desc,
                category_block_asc)
            Option.create_from_block(poll, option_block)
            return poll
        else:
            raise NonUniqueError("You can't use the same poll name twice "
                "in the same event. Please choose another name.",
                "title_error")


class Option(models.Model):
    poll = models.ForeignKey("Poll", related_name="options")
    title = models.CharField(max_length=500, unique=True)

    @classmethod
    def unique_title(cls, poll, test_title):
        options = cls.objects.filter(poll=poll)
        for option_title in [option.title.lower() for option in options]:
            if option_title == test_title.lower():
                return False
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
                    poll.delete()
                    categories = Category.objects.filter(poll=poll)
                    categories.delete()
                    options = cls.objects.filter(poll=poll)
                    options.delete()
                    raise NonUniqueError(
                        "You can't use the same option name twice in the "
                        "same poll. Please choose another name.",
                        "option_error")


class Category(models.Model):
    poll = models.ForeignKey("Poll", related_name="categories")
    title = models.CharField(max_length=500)
    best_possible_rating = models.IntegerField(default=3)

    @classmethod
    def unique_title(cls, poll, test_title):
        cats = cls.objects.filter(poll=poll)
        for cat_title in [cat.title.lower() for cat in cats]:
            if cat_title == test_title.lower():
                return False
        return True

    @classmethod
    def create_from_blocks(cls, poll, block_desc, block_asc):
        cls.create_from_block(poll, block_desc, "desc")
        cls.create_from_block(poll, block_asc, "asc")

    @classmethod
    def create_from_block(cls, poll, block, asc_or_desc):
        for item in block.split('\r\n'):
            if item:
                item_dict = item.split(',')
                category = cls(poll=poll)
                category.title = item_dict[0].strip()
                if asc_or_desc == "asc":
                    category.best_possible_rating = 1
                else:
                    category.best_possible_rating = 3
                if cls.unique_title(poll, category.title):
                    category.save()
                else:
                    poll.delete()
                    categories = cls.objects.filter(poll=poll)
                    categories.delete()
                    raise NonUniqueError(
                        "You can't use the same category name twice in the "
                        "same poll. Please choose another name.",
                        "category_error")


class NonUniqueError(Exception):
    def __init__(self, value, type):
        self.value = value
        self.type = type

    def __str__(self):
        return repr(self.value)
