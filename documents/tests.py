from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import Client
from core.models import Criterion
from oauth2_provider.models import Application
import json


# Create your tests here.

class DocumentsApiTestCase(TestCase):
	def setUp(self):
		get_user_model().objects.create_user(username = "naty", password="naty")
		get_user_model().objects.create_user(username = "mario", password="mario")
		Criterion.objects.create(
			name = "criterion1",
			description = "si",
			upload_cost = 10,
			download_cost = 20,
			challenge_reward = 30)
		Criterion.objects.create(
			name = "criterion2",
			description = "si",
			upload_cost = 10,
			download_cost = 20,
			challenge_reward = 30)
		application = Application.objects.create(
			client_id = "asdf1234",
			client_secret = "qwerty1234",
			user_id = 1,
			authorization_grant_type = "password",
			client_type = "secret")


	def get_token(self):
		c = Client()
		response = c.post('/o/token/',
			{'client_id' : 'asdf1234',
			 'client_secret' : 'qwerty1234',
			 'grant_type' : 'password',
			 'username' : 'naty',
			 'password' : 'naty'})
		parsed_response = json.loads(response.content)
		token = parsed_response['access_token']		
		return token


	def test_create_document(self):
		c = Client()
		response1 = c.post('/api/v1.0/apps/',
			{'name' : 'app', 'description' : 'description1', 'developers' : '["naty", "mario"]',
			 'criteria' : '["criterion1", "criterion2"]'})

		token = self.get_token()
		auth_header = {
			'HTTP_AUTHORIZATION' : 'Bearer ' + token,
		}

		response2 = c.post('/api/v1.0/documents/',
			{'name' : 'document', 'description' : 'description',
			 'creator' : 'naty', 'app' : 'app', 'criteria' : '["criterion1", "criterion2"]'},
			 **auth_header)
		
		status = json.loads(response2.content)['status']
		self.assertEqual('ok', status)


	#def test_download_document(self):
