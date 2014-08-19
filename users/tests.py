from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test.utils import override_settings
from core.models import Criterion
from users.models import Punctuation
from django.test import Client
from django.contrib.auth.models import User
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
		
	def test_user_login(self):
		c=Client()
		username = "naty"
		password = "naty"
		response = c.post('/api/v1.0/users/login/',{'username' : username, 'password' : password})
		status = json.loads(response.content)['status']
		error = json.loads(response.content)['error']
		self.assertEqual('logged_in',status)

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

	def test_get_punctuation_created_registry(self):
		c = Client()
		response = c.get('/api/v1.0/users/punctuation/',
			{'username' : 'zebhid', 'criterion' : 'criterio 1'})
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
		response = c.get('/api/v1.0/users/punctuation/',
			{'username' : 'zebhid', 'criterion' : 'criterio 3'})
		parsed_response = json.loads(response.content)
		self.assertEqual('ok',parsed_response['status'])
		self.assertEqual(0,parsed_response['data']['score'])

	def test_get_punctuation_wrong_request(self):
		"""el usuario o el criterion no existen"""
		c = Client()
		response = c.get('/api/v1.0/users/punctuation/',
			{'username' : 'zebhid', 'criterion' : 'no existo'})
		response2 = c.get('/api/v1.0/users/punctuation/',
			{'username' : 'no existo', 'criterion' : 'criterio 1'})
		parsed_response = json.loads(response.content)
		parsed_response1 = json.loads(response2.content)
		self.assertEqual('user or criterion does not exists',parsed_response['error'])
		self.assertEqual('user or criterion does not exists',parsed_response1['error'])
