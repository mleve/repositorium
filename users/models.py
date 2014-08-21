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

	def update_punctuation(self,option):
		if option == "download":
			cost = self.criterion.download_cost
			if self.credit < cost:
				return False
			else:
				self.credit = self.credit - cost
				self.score = self.score + cost
				return True
		elif option == "upload":
			cost = self.criterion.upload_cost
			if self.credit < cost:
				return False
			else:
				self.credit = self.credit - cost
				self.score = self.score + cost
				return True



	class Meta:
		unique_together = (("user","criterion"),)

