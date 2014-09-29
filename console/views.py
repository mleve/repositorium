from django.shortcuts import render_to_response,render
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from core.models import App
from console.forms import AppForm


# Create your views here.

@login_required()
def home(request):
	apps = App.objects.filter(developers = request.user)
	return render_to_response('logged_welcome.html',
		{'apps' : apps},
		 context_instance=RequestContext(request))


@login_required()
def create_app(request):
	if request.method == 'POST':
		form = AppForm(request.POST)
		if form.is_valid():
			form.save()
			#TODO create app in oauth to get client_id and secret
			return HttpResponse("ok", content_type='plain/text')
	else:
		form = None
		if request.GET.has_key("app_id"):
			app = App.objects.get(id = request.GET['app_id'])
			form = AppForm(instance = app)
		else:
			form = AppForm()
	return render(request, 'console/forms/app.html',{'app_form' : form})

@login_required()
def list_apps(request):
	apps = App.objects.filter(developers = request.user)
	return render_to_response('console/list_apps.html',
		{'apps' : apps},
		context_instance = RequestContext(request))