from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Criterion(models.Model):
	name = models.CharField(max_length=45, unique=True)
	description = models.TextField()
	upload_cost = models.IntegerField(default = 10)
	download_cost = models.IntegerField(default = 10)
	challenge_reward = models.IntegerField(default = 10)
	experts = models.ManyToManyField(User)
	def __unicode__(self):
		return self.name

class App(models.Model):
	name = models.CharField(max_length=45, unique=True)
	description = models.TextField()
	developers = models.ManyToManyField(User)
	criteria = models.ManyToManyField(Criterion)
	def __unicode__(self):
		return self.name