from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Criterion, App
from django.test import Client
import json

# Create your tests here.

class AppsApiTestCase(TestCase):
	def setUp(self):
		get_user_model().objects.create_user(username = "naty", password="naty")
		get_user_model().objects.create_user(username = "mario", password="mario")
		Criterion.objects.create(
			name = "criterio1",
			description = "si",
			upload_cost = 10,
			download_cost = 20,
			challenge_reward = 30)
		Criterion.objects.create(
			name = "criterio2",
			description = "si",
			upload_cost = 10,
			download_cost = 20,
			challenge_reward = 30)



	def test_create_app(self):
		c = Client()
		response = c.post('/api/v1.0/apps/',
			{'name' : 'app', 'description' : 'lalala', 'developers' : '["naty", "mario"]',
			 'criteria' : '["criterio1", "criterio2"]'})
		status = json.loads(response.content)['status']

		self.assertEqual('ok', status)


		app = App.objects.get(name = 'app')

		self.assertEqual('lalala', app.description)

