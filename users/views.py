from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
#from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import  MultiValueDictKeyError
from users.models import Punctuation
from core.models import Criterion
import json
# Create your views here.

#@csrf_exempt
def login(request):
	if(request.method == 'POST'):
		response = {}
		if check_parameters(request.POST,['username','password']) == False:
			response['status'] = 'error'
			response['error'] = 'missing parameters, include username and password'
			return HttpResponse(json.dumps(response),content_type='application/json')

		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username = username, password = password)
		if user is not None:
			if user.is_active:
				response['status'] = 'logged_in'
				response['error'] = ''
			else:
				response['status'] = 'error'
				response['error'] = 'user is not active'
		else:
			response['status'] = 'error'
			response['error'] = 'username or password incorrect'
		return HttpResponse(json.dumps(response),content_type='application/json')

def get_punctuation(request):
	response = {}

	if check_parameters(request.GET,['username','criterion']) == False:
		response['status'] = 'error'
		response['error'] = 'missing parameters, include username and criterion'
		return HttpResponse(json.dumps(response),content_type='application/json')
	

	username = request.GET['username']
	criterion = request.GET['criterion']
	try:
		user_obj = User.objects.get(username = username)
		criterion_obj = Criterion.objects.get(name = criterion)
		try:
			punctuation = Punctuation.objects.get(user = user_obj, criterion = criterion_obj)
		except ObjectDoesNotExist:
			punctuation = Punctuation.objects.create(
				user = user_obj, 
				criterion = criterion_obj)
		response['status'] = 'ok'
		data = {}
		data['score'] = punctuation.score
		data['credit'] = punctuation.credit
		data['failure_rate'] = punctuation.failure_rate
		response['data'] = data
	except ObjectDoesNotExist:
		response['status'] = 'error'
		response['error'] = 'user or criterion does not exists'
	
	return HttpResponse(json.dumps(response),content_type='application/json')

def check_parameters(request_params_dict, params_list):
	for param in params_list:
		if request_params_dict.has_key(param) == False:
			return False
	return True
		


