from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Criterion, App
from django.test import Client
from oauth2_provider.models import Application
import json
from repositorium.auxiliar import get_auth_header


# Create your tests here.

class AppsApiTestCase(TestCase):
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


	def test_create_app(self):
		c = Client()
		response = c.post('/api/v1.0/apps/',
			{'name' : 'app', 'description' : 'description1', 'developers' : '["naty", "mario"]',
			 'criteria' : '["criterion1", "criterion2"]'})
		
		status = json.loads(response.content)['status']
		self.assertEqual('ok', status)
		app = App.objects.get(name = 'app')
		self.assertEqual('description1', app.description)


	def test_create_duplicated_app(self):
		c = Client()
		response1 = c.post('/api/v1.0/apps/',
			{'name' : 'app', 'description' : 'description1', 'developers' : '["naty", "mario"]',
			 'criteria' : '["criterion1", "criterion2"]'})
		
		status1 = json.loads(response1.content)['status']
		self.assertEqual('ok', status1)

		response2 = c.post('/api/v1.0/apps/',
			{'name' : 'app', 'description' : 'description1', 'developers' : '["naty", "mario"]',
			 'criteria' : '["criterion1", "criterion2"]'})
		
		status2 = json.loads(response2.content)
		self.assertEqual('error', status2['status'])
		self.assertEqual('Name already used', status2['error'])


	def test_empty_developers(self):
		c = Client()
		response = c.post('/api/v1.0/apps/',
			{'name' : 'app', 'description' : 'description1', 'developers' : '[]',
			 'criteria' : '["criterion1", "criterion2"]'})
		
		status = json.loads(response.content)
		self.assertEqual('error', status['status'])
		self.assertEqual('List of developers or list of criteria empty', status['error'])


	def test_empty_criteria(self):
		c = Client()
		response = c.post('/api/v1.0/apps/',
			{'name' : 'app', 'description' : 'description1', 'developers' : '["naty", "mario"]',
			 'criteria' : '[]'})
		
		status = json.loads(response.content)
		self.assertEqual('error', status['status'])
		self.assertEqual('List of developers or list of criteria empty', status['error']) 


	def test_developer_not_in_bd(self):
		c = Client()
		response = c.post('/api/v1.0/apps/',
			{'name' : 'app', 'description' : 'description1', 'developers' : '["lal", "mario"]',
			 'criteria' : '["criterion1", "criterion2"]'})
		
		status = json.loads(response.content)
		self.assertEqual('error', status['status'])
		self.assertEqual('Some of your developers are not in the db', status['error']) 


	def test_criterion_not_in_db(self):
		c = Client()
		response = c.post('/api/v1.0/apps/',
			{'name' : 'app', 'description' : 'description1', 'developers' : '["naty", "mario"]',
			 'criteria' : '["criterion1", "criterion2", "criterio3"]'})
		
		status = json.loads(response.content)
		self.assertEqual('error', status['status'])
		self.assertEqual('Some of your criteria are not in the db', status['error'])



class CriteriaApiTestCase(TestCase):
	def setUp(self):
		get_user_model().objects.create_user(username = "naty", password="naty")


	def test_create_criterion(self):
		c = Client()
		response = c.post('/api/v1.0/criteria/',
			{'name' : 'criterion', 'description' : 'description1', 'expert' : 'naty'})

		status = json.loads(response.content)['status']
		self.assertEqual('ok', status)

		app = Criterion.objects.get(name = 'criterion')


	def test_create_duplicated_criterion(self):
		c = Client()
		response1 = c.post('/api/v1.0/criteria/',
			{'name' : 'criterion', 'description' : 'description1', 'expert' : 'naty'})

		status1 = json.loads(response1.content)['status']
		self.assertEqual('ok', status1)

		response2 = c.post('/api/v1.0/criteria/',
			{'name' : 'criterion', 'description' : 'description2', 'expert' : 'naty'})
		
		status2 = json.loads(response2.content)
		self.assertEqual('error', status2['status'])
		self.assertEqual('Name already used', status2['error'])
	

	def test_expert_not_in_bd(self):
		c = Client()
		response = c.post('/api/v1.0/criteria/',
			{'name' : 'criterion', 'description' : 'description', 'expert' : 'mario'})
		
		status = json.loads(response.content)
		self.assertEqual('error', status['status'])
		self.assertEqual('The expert is not in the db', status['error'])

class ChallengeApiTestCase(TestCase):
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

		Document.objects.create(
			name = "document_test",
			description = "Document for testing",
			creator = get_user_model().objects.get(username = "naty"))
		Document.objects.create(
			name = "document_test_2",
			description = "Naty is not my owner :@",
			creator = get_user_model().objects.get(username = "mario"))

		

		application = Application.objects.create(
			client_id = "asdf1234",
		 	client_secret = "qwerty1234",
		 	user_id = 1,
		 	authorization_grant_type = "password",
		 	client_type = "secret")


	def test_get_challenge(self):
		c = Client()

		response = c.get('/api/v1.0/criteria/challenge/',
			{'criterion' : 'criterion1'},
			**get_auth_header('mario','mario'))

		self.assertEqual("no",response)
		parsed_response = json.loads(response.content)

		self.assertEqual("ok",parsed_response['status'])

		#checks get 4 document in the response
		self.assertEqual(4,len(parsed_response[data].documents))

