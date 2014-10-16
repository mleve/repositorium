from users.models import Punctuation
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import  MultiValueDictKeyError
from django.test import Client
import json
#obtain or create a punctuation record
def aux_get_punctuation(user,criterion):
		try:
			punctuation = Punctuation.objects.get(user = user, criterion = criterion)
		except ObjectDoesNotExist:
			punctuation = Punctuation.objects.create(
				user = user, 
				criterion = criterion)
		return punctuation	

#check if the get or post request includes all the params listed in params_list
def check_parameters(request_params_dict, params_list):
	for param in params_list:
		if request_params_dict.has_key(param) == False:
			return False
	return True

def get_token(username,password):
		c = Client()
		response = c.post('/o/token/',
			{'client_id' : 'asdf1234',
			 'client_secret' : 'qwerty1234',
			 'grant_type' : 'password',
			 'username' : username,
			 'password' : password})
		parsed_response = json.loads(response.content)
		token = parsed_response['access_token']		
		return token

def get_auth_header(username,password):
		return {'HTTP_AUTHORIZATION' : 'Bearer '+ get_token(username,password)}