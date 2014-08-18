from django.http import HttpResponse
from django.contrib.auth import authenticate
#from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
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