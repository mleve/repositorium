from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from users.models import Punctuation
from core.models import Criterion
from documents.models import Document, File,Fullfill
import json, datetime


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
	criteria_list = []
	for criterion in list_of_criteria:
		criterion_obj = Criterion.objects.get(name = criterion)
		criteria_list.append(criterion_obj)
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

	#indicate that the document meets the criteria
	create_fulfill(document,criteria_list)

	return HttpResponse(json.dumps(response), content_type='application/json')

def create_fulfill(document,criteria):
	for criterion in criteria:
		Fullfill.objects.create(
			criterion = criterion,
			document = document,
			status = 1,
			positive = 0,
			negative = 0,
			validated_date = datetime.date.today()
			)
	return True


@login_required
def upload_file(request):
	# Checks Document existence
	doc_name = request.POST['document_name']
	
	response = {}

	if Document.objects.filter(name = doc_name).exists():
		document = Document.objects.get(name= doc_name)
		# Checks user is owner of the document
		if document.creator.id == request.user.id:

			size_ok = True;

			#Checks size of the documents
			for filename, file in request.FILES.iteritems():
				#Max size 50 Mb
				if not file.size != 0 and file.size <= 51200:
					size_of = False
					response['status'] = 'error'
					response['error'] = 'Some of your files are empty or too big to be uploaded'
					return HttpResponse(json.dumps(response), content_type='application/json')	

			# Transfer to final destination
			for filename, file in request.FILES.iteritems():
				File.objects.create(document=document,value=file)
			response['status'] = 'ok'
		else:
			response['status'] = 'error'
			response['error'] = 'You are not the owner of this document'
	else:
		response['status'] = "error"
		response['error'] = "Document doesn't exists"

		#Create file record
	return HttpResponse(json.dumps(response),content_type='application/json')


#@login_required
#def download_file(request):
	# Check Document existence
#	doc_name = request.POST['document_name']