from django.shortcuts import render
from django.http import HttpResponse
from app.models import User
import random
import requests
import json

# App home page.
def home(request):
	# Grab super key, and a list of all convos to display before joining a conversation
	super_key = 'Layer session-token='+request.session['super_key']
	superHeaders = {'Accept':'application/vnd.layer+json; version=1.0', 'Authorization': super_key}
	r = requests.get('https://api.layer.com/conversations', headers=superHeaders)
	superdic = json.loads(r.text)
	print super_key

	# Grab all personal conversations (i.e one's a user is currently in)
	personal_key = 'Layer session-token='+request.session['layer_sessionid']
	personalHeaders = {'Accept':'application/vnd.layer+json; version=1.0', 'Authorization': personal_key}
	r2 = requests.get('https://api.layer.com/conversations', headers=personalHeaders)
	personaldic=json.loads(r2.text)

	#Test to see if user is logged in, and if so, save all contexts (including a silly message)
	try:
		welcmess=['Hey there,', 'Welcome,', 'Hi', 'Gday', 'Hello', 'Greetings', 'Howdy', 'Hi-ya,', "Yo", "Heya",'Aloha']
		c = {'welcome':random.choice(welcmess), 'name': request.session['first'], 'img':request.session['profpic'],'convolist':superdic, 'personallist': personaldic}
	except KeyError:
		return HttpResponse("Nice try fucker you're not logged in. Also possible is that i made a mistake in which case sorry?")
	template = 'apphome.html'
	return render(request, template, c)

#Depreciated - add you to a convo, display all parts
def convo(request):
	convoid = request.GET.get('convoid')
	try:
		url = convoid+'/messages'
		layerAuth = 'Layer session-token='+request.session['layer_sessionid']
		headers = {'Accept':'application/vnd.layer+json; version=1.0', 'Authorization': layerAuth}
		r = requests.get(url, headers = headers)
		detes = json.loads(r.text)
		dastring = ""
		count = 10
		while (count>-1):
			try:
				name = User.objects.get(pk=detes[count]['sender']['user_id'])
				dastring = dastring + "<p>"+ name.full() + ": " + str(detes[count]['parts'][0]["body"])+ "</p>"
				count = count -1
			except IndexError:
				count = count - 1

	except KeyError:
		url = convoid
		layerAuth = 'Layer session-token='+request.session['super_key']
    	headers = {'Accept':'application/vnd.layer+json; version=1.0', 'Authorization': layerAuth, "Content-Type": "application/vnd.layer-patch+json"}
    	data = [{"operation": "add", "property": "participants", "value":request.session['id']}]
    	r = requests.patch(url, headers=headers, json=data)
    	url = convoid+'/messages'
    	layerAuth = 'Layer session-token='+request.session['layer_sessionid']
    	headers = {'Accept':'application/vnd.layer+json; version=1.0', 'Authorization': layerAuth}
    	r = requests.get(url, headers = headers)
    	detes = json.loads(r.text)
    	dastring = ""
    	# print request.session['super_key']
    	count = 10
    	while (count>-1):
    		try:
    			name = User.objects.get(pk=detes[count]['sender']['user_id'])
    			dastring = dastring + "<p>"+ name.full() + ": " + str(detes[count]['parts'][0]["body"])+ "</p>"
    			count = count -1
    		except IndexError:
    			count = count - 1

	c = {'convo':dastring, 'url':url, 'seshid':request.session['layer_sessionid']}
	template='convo.html'
	return render(request, template, c)


def first_login(request):
	c={}
	template="first_login.html"
	return render(request, template, c)

#Save all info to the database
def setup(request):
	pic = request.session['profpic']
	if pic is None:
		pic = "https://c2.staticflickr.com/6/5122/5281085848_dceaed6ffc.jpg"
	u = User(first_name=request.session['first'],last_name=request.session['last'],prof_pic=pic,first_log_in=True, email1=request.session['email'], idnumber=request.session['id'])
	u.save()
	return HttpResponse('cool')

# Sign a user out (flushes session db)
def sign_out(request):
	request.session.flush()
	c ={}
	template="signedout.html"
	return render(request, template, c)

# Method to connect Google IDs to names in DB.
def id_to_name(request):
	name = User.objects.get(pk=request.GET.get('id'))
	name = name.full()
	return HttpResponse(str(name))


