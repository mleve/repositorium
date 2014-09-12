from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test.utils import override_settings
from core.models import Criterion
from users.models import Punctuation
from django.test import Client
from django.contrib.auth.models import User
from oauth2_provider.models import Application
import json


# Create your tests here.

class PunctuationsTestCase(TestCase):
	def setUp(self):
		get_user_model().objects.create_user(username = "zebhid", password="qwf5xp")
		get_user_model().objects.create_user(username = "john", password="qwerty")
		Criterion.objects.create(
			name = "criterio 1",
			description = "si",
			upload_cost = 10,
			download_cost = 20,
			challenge_reward = 30)
		Criterion.objects.create(
			name = "criterio 2",
			description = "si",
			upload_cost = 10,
			download_cost = 20,
			challenge_reward = 30)


	def test_update_punctuation_download(self):
		zebhid = get_user_model().objects.get(username="zebhid")
		criterion1 = Criterion.objects.get(name="criterio 1")
		punctuation = Punctuation.objects.create(
			user = zebhid,
			criterion = criterion1,
			score=5,
			credit=3,
			failure_rate=3)
		response = punctuation.update_punctuation("download")
		self.assertEqual(False, response)

		criterion2 = Criterion.objects.get(name="criterio 2")
		punctuation2 = Punctuation.objects.create(
			user = zebhid,
			criterion = criterion2,
			score=0,
			credit=20,
			failure_rate=3)
		response = punctuation2.update_punctuation("download")
		self.assertEqual(True, response)
		new_punctuation = Punctuation.objects.get(user=zebhid,criterion=criterion2)
		self.assertEqual(20,new_punctuation.score)
		

	def test_update_punctuation_upload(self):
		zebhid = get_user_model().objects.get(username="zebhid")
		criterion1 = Criterion.objects.get(name="criterio 1")
		punctuation = Punctuation.objects.create(
			user = zebhid,
			criterion = criterion1,
			score=5,
			credit=3,
			failure_rate=3)
		response = punctuation.update_punctuation("upload")
		self.assertEqual(False, response)

		criterion2 = Criterion.objects.get(name="criterio 2")
		punctuation2 = Punctuation.objects.create(
			user = zebhid,
			criterion = criterion2,
			score=0,
			credit=20,
			failure_rate=3)
		response = punctuation2.update_punctuation("upload")
		self.assertEqual(True, response)
		new_punctuation = Punctuation.objects.get(user=zebhid,criterion=criterion2)
		self.assertEqual(10,new_punctuation.score)
		self.assertEqual(10,new_punctuation.credit)


	def test_update_punctuation_challengue(self):
		zebhid = get_user_model().objects.get(username="zebhid")
		criterion1 = Criterion.objects.get(name="criterio 1")
		punctuation = Punctuation.objects.create(
			user = zebhid,
			criterion = criterion1,
			score=0,
			credit=0,
			failure_rate=0)
		response = punctuation.update_punctuation("challenge_fail")
		self.assertEqual(True, response)
		new_punctuation = Punctuation.objects.get(user=zebhid,criterion=criterion1)
		self.assertEqual(0,new_punctuation.credit)
		self.assertEqual(1,new_punctuation.failure_rate)

		criterion2 = Criterion.objects.get(name="criterio 2")
		punctuation2 = Punctuation.objects.create(
			user = zebhid,
			criterion = criterion2,
			score=0,
			credit=0,
			failure_rate=2)
		response = punctuation2.update_punctuation("challenge_success")
		self.assertEqual(True, response)
		new_punctuation = Punctuation.objects.get(user=zebhid,criterion=criterion2)
		self.assertEqual(30,new_punctuation.credit)
		self.assertEqual(1,new_punctuation.failure_rate)


	def test_normal_creation(self):
		zebhid = get_user_model().objects.get(username="zebhid")
		john = get_user_model().objects.get(username="john")
		criterion1 = Criterion.objects.get(name="criterio 1")
		criterion2 = Criterion.objects.get(name="criterio 2")

		Punctuation.objects.create(
			user = zebhid,
			criterion = criterion1,
			score=5,
			credit=3,
			failure_rate=3)

		score = Punctuation.objects.get(user = zebhid, criterion = criterion1).score
		self.assertEqual(score,5)


	def test_no_duplicate_creation(self):
		zebhid = get_user_model().objects.get(username="zebhid")
		john = get_user_model().objects.get(username="john")
		criterion1 = Criterion.objects.get(name="criterio 1")
		criterion2 = Criterion.objects.get(name="criterio 2")

		Punctuation.objects.create(
			user = zebhid,
			criterion = criterion1,
			score=5,
			credit=3,
			failure_rate=3)
		
		self.assertRaises(IntegrityError,
			Punctuation.objects.create,
			user = zebhid,
			criterion = criterion1,
			score=5,
			credit=3,
			failure_rate=3)



class UsersApiTestCase(TestCase):
	def setUp(self):
		get_user_model().objects.create_user(username = "mario", password="mario")
		get_user_model().objects.create_user(username = "naty", password="naty")
	"""
	def test_user_login(self):
		c=Client()
		username = "naty"
		password = "naty"
		response = c.post('/api/v1.0/users/login/',{'username' : username, 'password' : password})
		status = json.loads(response.content)['status']
		error = json.loads(response.content)['error']
		self.assertEqual('logged_in',status)
	"""



class PunctuationsApiTestCase(TestCase):
	def setUp(self):
		get_user_model().objects.create_user(username = "zebhid", password="qwf5xp")
		get_user_model().objects.create_user(username = "john", password="qwerty")
		Criterion.objects.create(
			name = "criterio 1",
			description = "si",
			upload_cost = 10,
			download_cost = 20,
			challenge_reward = 30)
		Criterion.objects.create(
			name = "criterio 2",
			description = "si",
			upload_cost = 10,
			download_cost = 20,
			challenge_reward = 30)
		zebhid = get_user_model().objects.get(username="zebhid")
		criterion1 = Criterion.objects.get(name="criterio 1")

		Punctuation.objects.create(
			user = zebhid,
			criterion = criterion1,
			score=10,
			credit=10,
			failure_rate=10)

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
			 'username' : 'zebhid',
			 'password' : 'qwf5xp'})
		parsed_response = json.loads(response.content)
		token = parsed_response['access_token']		
		return token


	def test_get_oauth2_token(self):
		c = Client()
		token = self.get_token()
		auth_header = {
			'HTTP_AUTHORIZATION' : 'Bearer ' + token,
		}

		response = c.get('/si/',
			{},
			**auth_header)
		self.assertEqual("hola",response.content)


	def test_get_punctuation_created_registry(self):
		c = Client()
		token = self.get_token()
		auth_header = {
			'HTTP_AUTHORIZATION' : 'Bearer ' + token,
		}		
		response = c.get('/api/v1.0/users/punctuation/',
			{'username' : 'zebhid', 'criterion' : 'criterio 1'},
			**auth_header)
		parsed_response = json.loads(response.content)
		self.assertEqual('ok',parsed_response['status'])
		self.assertEqual(10,parsed_response['data']['score'])


	def test_get_punctuation_new_registry(self):
		Criterion.objects.create(
			name = "criterio 3",
			description = "si",
			upload_cost = 10,
			download_cost = 20,
			challenge_reward = 30)
		c = Client()
		token = self.get_token()
		auth_header = {
			'HTTP_AUTHORIZATION' : 'Bearer ' + token,
		}		
		response = c.get('/api/v1.0/users/punctuation/',
			{'username' : 'zebhid', 'criterion' : 'criterio 3'},
			**auth_header)
		parsed_response = json.loads(response.content)
		self.assertEqual('ok',parsed_response['status'])
		self.assertEqual(0,parsed_response['data']['score'])


	def test_get_punctuation_wrong_request(self):
		"""el usuario o el criterion no existen"""
		c = Client()
		token = self.get_token()
		auth_header = {
			'HTTP_AUTHORIZATION' : 'Bearer ' + token,
		}		
		response = c.get('/api/v1.0/users/punctuation/',
			{'criterion' : 'no existo'},
			**auth_header)
		response2 = c.get('/api/v1.0/users/punctuation/',
			{},
			**auth_header)

		parsed_response = json.loads(response.content)
		parsed_response2 = json.loads(response2.content)
		
		self.assertEqual('criterion does not exists',parsed_response['error'])
		self.assertEqual('missing parameters, include criterion',parsed_response2['error'])