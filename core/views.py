from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from core.models import App, Criterion
from django.contrib.auth.decorators import login_required
from repositorium.auxiliar import aux_get_punctuation, check_parameters
from documents.models import Document, Fullfill
import json

# Create your views here.

def create_app(request):
	response = {}
	name = request.POST['name']
	description = request.POST['description']
	developers_names = json.loads(request.POST['developers'])
	list_of_criteria = json.loads(request.POST['criteria'])
	
	#Check if there is no app with the same name
	if App.objects.filter(name = name).exists():
		response['status'] = 'error'
		response['error'] = 'Name already used'
		return HttpResponse(json.dumps(response), content_type='application/json') 

	else:
		#Check that the list of developers and the list of criteria are not empty
		if developers_names and list_of_criteria:

			developers_ok = True
			criteria_ok = True

			#Check that the developers are in the db
			for developer in developers_names:
				if not get_user_model().objects.filter(username = developer).exists():
					developers_ok = False
					response['status'] = 'error'
					response['error'] = 'Some of your developers are not in the db'
					return HttpResponse(json.dumps(response), content_type='application/json')

			#Checks that the criteria are in the db
			for criterion in list_of_criteria:
				if not Criterion.objects.filter(name = criterion).exists():
					criteria_ok = False
					response['status'] = 'error'
					response['error'] = 'Some of your criteria are not in the db'
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
			response['error'] = 'List of developers or list of criteria empty'
			return HttpResponse(json.dumps(response), content_type='application/json')


def create_criterion(request):
	response = {}
	name = request.POST['name']
	description = request.POST['description']
	#It is assumed that that the user who creates the criterion is the expert of it
	expert = request.POST['expert']

	#Checks that there is no app with the same name
	if Criterion.objects.filter(name = name).exists():
		response['status'] = 'error'
		response['error'] = 'Name already used'
		return HttpResponse(json.dumps(response), content_type='application/json') 

	else:
		#Checks that the expert is not empty
		if expert:

			expert_ok = True

			#Checks that the expert is in the db
			if not get_user_model().objects.filter(username = expert).exists():
				expert_ok = False
				response['status'] = 'error'
				response['error'] = 'The expert is not in the db'
				return HttpResponse(json.dumps(response), content_type='application/json')

		criterion = Criterion.objects.create(name = name, description = description)
		criterion.experts.add(get_user_model().objects.get(username = expert))

		response['status'] = 'ok'
		return HttpResponse(json.dumps(response), content_type='application/json')

@login_required
def create_challenge(request):
	response = {}

	user = request.user
	if check_parameters(request.GET,['criterion']) == False:
		response['status'] = 'error'
		response['error'] = 'Missing parameters, include criterion'
		return HttpResponse(json.dumps(response),content_type='application/json')

	criterion = Criterion.objects.get(name = request.GET['criterion'])

	#get user failure rate
	punctuation = aux_get_punctuation(user,criterion)
	fail_rate = punctuation.failure_rate
	#create challenge record
	n_known_docs = 2 + fail_rate
	n_unknown_docs = 4 -n_known_docs

	fulfill = Fullfill.objects.filter(criterion = criterion).order_by('?')
	docs = []
	known_docs = []
	known_docs_id = []
	for i in range(0,n_known_docs):
		docs.append(fulfill[i].document)
		known_docs_id.append(fulfill[i].document.id)

	response['status'] = 'ok'
	data = {}
	data['documents'] = docs
	response['data'] = data





	#create response

	return HttpResponse(json.dumps(response), content_type='application/json')



