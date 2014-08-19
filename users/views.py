from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
#from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from users.models import Punctuation
from core.models import Criterion
import json
# Create your views here.

#@csrf_exempt
def login(request):
	if(request.method == 'POST'):
		response = {}
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
	username = request.GET['username']
	criterion = request.GET['criterion']
	response = {}

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