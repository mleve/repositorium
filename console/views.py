from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required()
def home(request):
	return render_to_response('list_apps.html', context_instance=RequestContext(request))
