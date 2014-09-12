from django.contrib.auth.models import User
from django.db import models
from core.models import Criterion
from django.core.exceptions import ValidationError


# Create your models here.

class Punctuation(models.Model):
	user = models.ForeignKey(User)
	criterion = models.ForeignKey(Criterion)
	score = models.IntegerField(default = 0)
	credit = models.IntegerField(default = 0)
	failure_rate = models.IntegerField(default = 0)
	def __unicode__(self):
		return self.user.username + " in " + self.criterion.name

	def update_punctuation(self,option):
		result = True
		if option == "download":
			cost = self.criterion.download_cost
			if self.credit < cost:
				result = False
			else:
				self.credit = self.credit - cost
				self.score = self.score + cost
		elif option == "upload":
			cost = self.criterion.upload_cost
			if self.credit < cost:
				result =  False
			else:
				self.credit = self.credit - cost
				self.score = self.score + cost
		elif option == "challenge_success":
			reward = self.criterion.challenge_reward
			self.credit = self.credit + reward
			self.score = self.score + reward
			self.update_failure_rate("decrease")
		elif option == "challenge_fail":
			self.update_failure_rate("increase")
		self.save()
		return result

	def update_failure_rate(self,option):
		prev_rate = self.failure_rate
		if option == "increase":
			if prev_rate < 2:
				self.failure_rate = prev_rate + 1
		else:
			if prev_rate > 0 :
				self.failure_rate = prev_rate - 1



	class Meta:
		unique_together = (("user","criterion"),)

