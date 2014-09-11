from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Document, File, Payment, Fullfill
from django.test import Client
import json

# Create your tests here.

class DocumentsApiTestCase(TestCase):
	def setUp(self):
		get_user_model().objects.create_user(username = "naty", password="naty")

	def test_download_document(self):


	def test_create_document(self):
		c = Client()
		response = c.post('/api/v1.0/documents/',
			{'name' : 'document', 'description' : 'description', 'creator' : 'naty'})
		status = json.loads(response.content)['status']

		self.assertEqual('ok', status)
