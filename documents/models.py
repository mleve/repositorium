from django.db import models
from django.contrib.auth.models import User

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