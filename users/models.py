from django.contrib.auth.models import User
from django.db import models
from core.models import Criterion
from django.core.exceptions import ValidationError


class Punctuation(models.Model):
	user = models.ForeignKey(User)
	criterion = models.ForeignKey(Criterion)
	score = models.IntegerField(default = 0)
	credit = models.IntegerField(default = 0)
	failure_rate = models.IntegerField(default = 0)
	def __unicode__(self):
		return self.user.username + " in " + self.criterion.name

	def update_punctuation(self):
		return "si"

	class Meta:
		unique_together = (("user","criterion"),)

