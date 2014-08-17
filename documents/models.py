from django.db import models
from django.contrib.auth.models import User

class Document(models.Model):
	name = models.CharField(max_length=45)
	description = models.TextField()
	creator = models.ManyToManyField(User)

class File(models.Model):
	document = models.ForeignKey(Document)
	value = models.FileField( upload_to = "document_extras")