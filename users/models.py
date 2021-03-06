from django.contrib.auth.models import User
from django.db import models
from core.models import Criterion
from django.core.exceptions import ValidationError


class Punctuation(models.Model):
	user = models.ForeignKey(User)
	criterion = models.ForeignKey(Criterion)
	score = models.IntegerField()
	credit = models.IntegerField()
	failure_rate = models.IntegerField()
	def __unicode__(self):
		return self.user.username + " in " + self.criterion.name

	class Meta:
		unique_together = (("user","criterion"),)

