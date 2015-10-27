from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
# Create your views here.

def home(request):
	template = loader.get_template('you/home.html')
	context = RequestContext(request, {
		})

	return HttpResponse(template.render(context))

def analyse(request,username):
	username="/u/"+username
	template = loader.get_template('you/you.html')
	context = RequestContext(request, {
		'username':username
		})

	return HttpResponse(template.render(context))