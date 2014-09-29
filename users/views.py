from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, render
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import  MultiValueDictKeyError
from users.models import Punctuation
from core.models import Criterion
from django.contrib.auth.forms import UserCreationForm
from users.forms import UserForm,LoginForm
import json


# Create your views here.
@login_required()
def get_punctuation(request):
	response = {}

	if check_parameters(request.GET,['criterion']) == False:
		response['status'] = 'error'
		response['error'] = 'Missing parameters, include criterion'
		return HttpResponse(json.dumps(response),content_type='application/json')
	

	#username = request.GET['username']
	criterion = request.GET['criterion']
	try:
		#user_obj = User.objects.get(username = username)
		user_obj = request.user
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
		response['error'] = 'Criterion does not exists'
	
	return HttpResponse(json.dumps(response),content_type='application/json')


def check_parameters(request_params_dict, params_list):
	for param in params_list:
		if request_params_dict.has_key(param) == False:
			return False
	return True


def create_user(request):
	if request.method == 'POST':
		form = UserForm(request.POST)
		if form.is_valid():
			new_user = get_user_model().objects.create_user(
				username = form.cleaned_data['username'],
				password = form.cleaned_data['password'])
			new_user.first_name = form.cleaned_data['name']
			new_user.last_name = form.cleaned_data['last_name']
			new_user.email = form.cleaned_data['email']
			new_user.save()

			user = authenticate(
				username=form.cleaned_data['username'],
				password=form.cleaned_data['password'])
			login(request,user)
			return HttpResponseRedirect('/home/')

	else:
		form = UserForm()
		form2  = LoginForm()

	return render(request, 'index.html',{'sign_in_form' : form, 'login_form' : form2})

def log_in(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			user = authenticate(username = form.cleaned_data['username'],
				 password = form.cleaned_data['password'])
			if user is not None:
				login(request,user)
				return HttpResponseRedirect('/home/')

	else:
		form = UserForm()
		form2  = LoginForm()

	return render(request, 'index.html',{'sign_in_form' : form, 'login_form' : form2})


