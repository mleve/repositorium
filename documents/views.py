from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from users.models import Punctuation
from core.models import Criterion, App
import json


# Create your views here.

@login_required()
def create_document(request):
	response = {}
	name = request.POST['name']
	description = request.POST['description']
	creator = request.user
	app = request.POST['app']

	#Checks if list of criteria belongs to the app
	criteria = request.POST['criteria']
	list_of_criteria = json.loads(criteria)

	criteria_ok = True

	#Checks if each criterion is in the db
	for criterion in list_of_criteria:
		if not criterion.objects.filter(name = criterion).exists():
			criteria_ok = False
			response['status'] = 'error'
			response['error'] = 'some of the criteria are not in the db'
			return HttpResponse(json.dumps(response), content_type='application/json')

	payment = True

	#Checks if the user has enough credit to pay for each criterion
	for criterion in list_of_criteria:
		try:
			punctuation = Punctuation.objects.get(user = creator, criterion = criterion)
		except ObjectDoesNotExist:
			punctuation = Punctuation.objects.create(user = creator, criterion = criterion)

		if not punctuation.credit >= punctuation.criterion.upload_cost
			payment = False
			response['status'] = 'error'
			response['error'] = "you don't have enouh credit to upload this document"
			return HttpResponse(json.dumps(response), content_type='application/json')	

	#Falta: pagar x criterio, crear documento

	#Check if user has enough credit to pay the upload_cost for each criterion
	#SearchLog.objects.get()


	#Funcion aparte para subir archivos

