from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import Client
from core.models import Criterion
from users.models import Punctuation
from documents.models import Document
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
		Document.objects.create(
			name = "document_test",
			description = "Document for testing",
			creator = get_user_model().objects.get(username = "naty"))
		Document.objects.create(
			name = "document_test_2",
			description = "Naty is not my owner :@",
			creator = get_user_model().objects.get(username = "mario"))


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


	def test_create_document_user_with_no_credit(self):
		c = Client()

		token = self.get_token()
		auth_header = {
			'HTTP_AUTHORIZATION' : 'Bearer ' + token,
		}

		response = c.post('/api/v1.0/documents/',
			{'name' : 'document', 'description' : 'description',
			 'creator' : 'mario', 'criteria' : '["criterion1", "criterion2"]'},
			 **auth_header)

		status = json.loads(response.content)
		self.assertEqual('error', status['status'])
		self.assertEqual("You don't have enough credit to upload this document", status['error'])



	def test_create_document_user_with_enough_credit(self):
		c = Client()

		token = self.get_token()
		auth_header = {
			'HTTP_AUTHORIZATION' : 'Bearer ' + token,
		}

		naty = get_user_model().objects.get(username="naty")
		criterion1 = Criterion.objects.get(name="criterion1")
		punctuation = Punctuation.objects.create(
			user = naty,
			criterion = criterion1,
			score=5,
			credit=10,
			failure_rate=3)
		criterion2 = Criterion.objects.get(name="criterion2")
		punctuation2 = Punctuation.objects.create(
			user = naty,
			criterion = criterion2,
			score=0,
			credit=10,
			failure_rate=3)		

		response = c.post('/api/v1.0/documents/',
			{'name' : 'document', 'description' : 'description',
			 'creator' : 'naty', 'criteria' : '["criterion1", "criterion2"]'},
			 **auth_header)

		status = json.loads(response.content)['status']
		self.assertEqual('ok', status)	


	def test_upload_file_with_normal_size(self):
		c = Client()
		token = self.get_token()
		auth_header = {
			'HTTP_AUTHORIZATION' : 'Bearer ' + token,
		}
		with open('requirements.txt') as fp:
			response = c.post('/api/v1.0/documents/files/', 
				{'document_name': 'document_test', 'nombre': fp},
				**auth_header)
	
		status = json.loads(response.content)['status']
		self.assertEqual('ok', status)


	def test_upload_file_with_unaccepted_size(self):
		c = Client()
		token = self.get_token()
		auth_header = {
			'HTTP_AUTHORIZATION' : 'Bearer ' + token,
		}
		with open('requirements2.txt') as fp:
			response = c.post('/api/v1.0/documents/files/', 
				{'document_name': 'document_test', 'nombre': fp},
				**auth_header)

		parsed_response = json.loads(response.content)
		status = parsed_response['status']
		error = parsed_response['error']
		self.assertEqual('Some of your files are empty or too big to be uploaded', error)	


	def test_upload_file_not_owner(self):
		c = Client()
		token = self.get_token()
		auth_header = {
			'HTTP_AUTHORIZATION' : 'Bearer ' + token,
		}
		with open('requirements.txt') as fp:
			response = c.post('/api/v1.0/documents/files/', 
				{'document_name': 'document_test_2', 'nombre': fp},
				**auth_header)
	
		parsed_response = json.loads(response.content)
		status = parsed_response['status']
		error = parsed_response['error']
		self.assertEqual('You are not the owner of this document', error)	


	def test_get_document(self):
		c = Client()
		token = self.get_token()
		auth_header = {
			'HTTP_AUTHORIZATION' : 'Bearer ' + token,
		}
		with open('requirements.txt') as fp:
			c.post('/api/v1.0/documents/files/', 
				{'document_name': 'document_test', 'nombre': fp},
				**auth_header)

		response = c.get('/api/v1.0/documents', {'document_name': 'document_test'})
		#Se recibe la metadata correctamente.

		#Obtener archivos adjuntos
		