from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from core.models import App


# Create your views here.

@login_required()
def home(request):
	apps = App.objects.filter(developers = request.user)
	return render_to_response('list_apps.html',
		{'apps' : apps},
		 context_instance=RequestContext(request))
