from django.db import models
from django.contrib.auth.models import User
from core.models import Criterion

class Document(models.Model):
	name = models.CharField(max_length=45, unique=True)
	description = models.TextField()
	creator = models.ManyToManyField(User)
	def __unicode__(self):
		return self.name

def get_document_name(instance,filename):
	return "/".join([instance.document.name,filename])

class File(models.Model):
	document = models.ForeignKey(Document)
	value = models.FileField( upload_to = get_document_name)
	def __unicode__(self):
		return self.value.name

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