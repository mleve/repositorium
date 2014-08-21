from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from core.models import App, Criterion

import json

# Create your views here.

def create_app(request):
	response = {}
	name = request.POST['name']
	description = request.POST['description']
	developers_names = json.loads(request.POST['developers'])
	list_of_criteria = json.loads(request.POST['criteria'])
	

	app = App.objects.create(name = name, description = description)

	for developer in developers_names:
		app.developers.add(get_user_model().objects.get(username = developer))

	for criterion in list_of_criteria:
		app.criteria.add(Criterion.objects.get(name = criterion))	

	response['status'] = 'ok'
	
	return HttpResponse(json.dumps(response),content_type='application/json')


	#check_parameters
	#ver que no exista una app con el mismo nombre
	#lista de developers != vacía y que los usuarios existan en la bd
	#lista de criterios != vacía y que los criterios existan en la bd
