from django.db import models
from django.contrib.auth.models import User
from core.models import Criterion, App


# Create your models here.

class Document(models.Model):
	name = models.CharField(max_length=45, unique=True)
	description = models.TextField()
	creator = models.ForeignKey(User)
	def __unicode__(self):
		return self.name

def get_file_name(instance,filename):
	return "/".join([instance.document.name,filename])


class File(models.Model):
	document = models.ForeignKey(Document)
	value = models.FileField( upload_to = get_file_name)
	def __unicode__(self):
		return self.value.name


class SearchLog(models.Model):
	user = models.ForeignKey(User)
	app_name = models.ForeignKey(App)
	criteria = models.TextField()
	class Meta:
		unique_together = (("user","app_name"),)


class Payment(models.Model):
	user = models.ForeignKey(User)
	document = models.ForeignKey(Document)
	class Meta:
		unique_together = (("user","document"),)
	def __unicode__(self):
		return self.user.username +" has paid for" + self.document.name


class Fullfill(models.Model):
	criterion = models.ForeignKey(Criterion)
	document = models.ForeignKey(Document)
	status = models.IntegerField()
	positive = models.IntegerField()
	negative = models.IntegerField()
	validated_date = models.DateField()
	class Meta:
		unique_together = (("criterion","document"),)