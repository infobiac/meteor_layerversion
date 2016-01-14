from django.shortcuts import render
from django.http import HttpResponseRedirect

#Landing page
def home(request):
	c={}
	template = "index.html"
	return render(request,template,c)

#Sending the newly logged in user to a temporary page while all info is saved (currently in layer_handlers)
def login(request):
	c={}
	template = "login.html"
	return render(request,template,c)

#What happens if you try to sign out with a non cmc address
def goaway(request):
	c={}
	template="goaway.html"
	return render(request,template,c)