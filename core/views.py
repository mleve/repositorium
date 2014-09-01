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
	
	#Comprobar que no existe una app con el mismo nombre
	if App.objects.filter(name = name).exists():
		response['status'] = 'error'
		response['error'] = 'name already used'
		return HttpResponse(json.dumps(response), content_type='application/json') 

	else:
		#Comprobar que la lista de developers y de criterios sea distinta de vacia
		if developers_names and list_of_criteria:

			developers_ok = True
			criteria_ok = True

			#Comprueba que los developers esten en la bd 
			for developer in developers_names:
				if not get_user_model().objects.filter(username = developer).exists():
					developers_ok = False
					response['status'] = 'error'
					response['error'] = 'some of your developers are not in the db'
					return HttpResponse(json.dumps(response), content_type='application/json')

			#Comprueba que los criterios estan en la bd
			for criterion in list_of_criteria:
				if not Criterion.objects.filter(name = criterion).exists():
					criteria_ok = False
					response['status'] = 'error'
					response['error'] = 'some of your criteria are not in the db'
					return HttpResponse(json.dumps(response), content_type='application/json')


			if developers_ok and criteria_ok:

				app = App.objects.create(name = name, description = description)

				for developer in developers_names:
					app.developers.add(get_user_model().objects.get(username = developer))

				for criterion in list_of_criteria:
					app.criteria.add(Criterion.objects.get(name = criterion))

				response['status'] = 'ok'
				return HttpResponse(json.dumps(response), content_type='application/json')

		else:
			response['status'] = 'error'
			response['error'] = 'list of developers or list of criteria empty'
			return HttpResponse(json.dumps(response), content_type='application/json')


def create_criterion(request):
	response = {}
	name = request.POST['name']
	description = request.POST['description']
	#Se asume que al crear un criterio el usuario que lo crea es el experto
	expert = request.POST['expert']

	#Comprobar que no existe una app con el mismo nombre
	if Criterion.objects.filter(name = name).exists():
		response['status'] = 'error'
		response['error'] = 'name already used'
		return HttpResponse(json.dumps(response), content_type='application/json') 

	else:
		#Comprueba que el experto no sea vacio
		if expert:

			expert_ok = True

			#Comprueba que el experto este en la bd 
			if not get_user_model().objects.filter(username = expert).exists():
				expert_ok = False
				response['status'] = 'error'
				response['error'] = 'the expert is not in the db'
				return HttpResponse(json.dumps(response), content_type='application/json')

		criterion = Criterion.objects.create(name = name, description = description)
		criterion.experts.add(get_user_model().objects.get(username = expert))

		response['status'] = 'ok'
		return HttpResponse(json.dumps(response), content_type='application/json')

		

