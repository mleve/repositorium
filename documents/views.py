from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from core.models import Document, File, Payment, Fullfill
import json

# Create your views here.

def create_document(request):
	response = {}
	name = request.POST['name']
	description = request.POST['description']
	creator = request.POST['creator']