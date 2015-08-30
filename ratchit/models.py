from django.db import models
from django.db.models import fields

class Event(models.Model):
	title = models.CharField(max_length=500, unique=True)

class Poll(models.Model):
	event = models.ForeignKey('Event', related_name='polls')
	title = models.CharField(max_length=500, unique=True)

	@classmethod
	def unique_title(cls, title):
		if Poll.objects.filter(title=title):
			return False
		else:
			return True

class Option(models.Model):
	poll = models.ForeignKey('Poll', related_name='options')
	title = models.CharField(max_length=500, unique=True)

	@classmethod
	def unique_title(cls, poll, title):
		if Option.objects.filter(title=title).filter(poll=poll):
			return False
		else:
			return True

class Category(models.Model):
	poll = models.ForeignKey('Poll', related_name='categories')
	title = models.CharField(max_length=500)
	best_possible_rating = models.IntegerField(default=3)

	@classmethod
	def unique_title(cls, poll, title):
		if Category.objects.filter(title=title).filter(poll=poll):
			return False
		else:
			return True

class Rater(models.Model):
	id_hash = models.CharField(max_length=32)

class Rating(models.Model):
	poll = models.ForeignKey('Poll', related_name='ratings')
	option = models.ForeignKey('Option', related_name='ratings')
	category = models.ForeignKey('Category', related_name='ratings')
	rater = models.ForeignKey('Rater', related_name='ratings')
	rating = models.IntegerField()
