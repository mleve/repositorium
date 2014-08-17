from django.contrib.auth.models import User
from django.db import models
from core.models import Criterion

class UserExtra(models.Model):
	user = models.OneToOneField(User)
	punctuations = models.ManyToManyField(Criterion, through = 'Punctuation')


class Punctuation(models.Model):
	user = models.ForeignKey(User)
	criterion = models.ForeignKey(Criterion)
	score = models.IntegerField()
	credit = models.IntegerField()
	failure_rate = models.IntegerField()

