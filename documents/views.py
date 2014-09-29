from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from users.models import Punctuation
from core.models import Criterion
from documents.models import Document
import json


# Create your views here.

@login_required()
def create_document(request):
	response = {}
	name = request.POST['name']
	description = request.POST['description']
	creator = request.user

	#Checks if list of criteria belongs to the app
	criteria = request.POST['criteria']
	list_of_criteria = json.loads(criteria)

	criteria_ok = True

	#Checks if each criterion is in the db
	for criterion in list_of_criteria:
		if not Criterion.objects.filter(name = criterion).exists():
			criteria_ok = False
			response['status'] = 'error'
			response['error'] = 'Some of the criteria are not in the db'
			return HttpResponse(json.dumps(response), content_type='application/json')

	payment = True

	#Checks if the user has enough credit to pay for each criterion
	for criterion in list_of_criteria:
		criterion_obj = Criterion.objects.get(name = criterion)
		try:
			punctuation = Punctuation.objects.get(user = creator, criterion = criterion_obj)
		except ObjectDoesNotExist:
			punctuation = Punctuation.objects.create(user = creator, criterion = criterion_obj)

		if not punctuation.credit >= punctuation.criterion.upload_cost:
			payment = False
			response['status'] = 'error'
			response['error'] = "You don't have enough credit to upload this document"
			return HttpResponse(json.dumps(response), content_type='application/json')

		punctuation.credit = punctuation.credit - punctuation.criterion.upload_cost


	#Create document
	document = Document.objects.create(name = name, description = description, creator = creator)
	response['status'] = 'ok'
	return HttpResponse(json.dumps(response), content_type='application/json')


	#Funcion aparte para subir archivos

