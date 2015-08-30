from django.db import models
from django.db.models import fields

class Event(models.Model):
	title = models.CharField(max_length=500)

class Poll(models.Model):
	event = models.ForeignKey('Event', related_name='polls')
	title = models.CharField(max_length=500)
	poll_type = models.CharField(max_length=500)

class Idea(models.Model):
	poll = models.ForeignKey('Poll', related_name='ideas')
	ordering = models.IntegerField()
	title = models.CharField(max_length=500)

class Category(models.Model):
	poll = models.ForeignKey('Poll', related_name='categories')
	title = models.CharField(max_length=500)
	best_possible_rating = models.IntegerField(default=3)

class Rater(models.Model):
	id_hash = models.CharField(max_length=32)

class Rating(models.Model):
	poll = models.ForeignKey('Poll', related_name='ratings')
	idea = models.ForeignKey('Idea', related_name='ratings')
	category = models.ForeignKey('Category', related_name='ratings')
	rater = models.ForeignKey('Rater', related_name='ratings')
	rating = models.IntegerField()
