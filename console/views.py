from django.shortcuts import render_to_response,render
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from core.models import App
from console.forms import AppForm


# Create your views here.

@login_required()
def home(request):
	apps = App.objects.filter(developers = request.user)
	return render_to_response('list_apps.html',
		{'apps' : apps},
		 context_instance=RequestContext(request))


@login_required()
def create_app(request):
	if request.method == 'POST':
		form = AppForm(request.POST)
		if form.is_valid():
			return HttpResponseRedirect('/home/')

	else:
		form = AppForm()
	return render(request, 'forms/app.html',{'app_form' : form})