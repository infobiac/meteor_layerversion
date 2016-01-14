# -*- coding: utf-8 -*-
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from layer import generate_identity_token
from django.shortcuts import render
from django.http import HttpResponse
from oauth2client import client, crypt
from app.models import User
import requests
import json
    
# disables the CSRF middleware, if you have it installed
@csrf_exempt
def get_identity_token(request):
    # check to ensure that we were given the req'd params
    if set(('user_id', 'nonce')) <= set(request.POST):
        user_id = request.POST['user_id']
        nonce = request.POST['nonce']
    else:
        return HttpResponse("Invalid Request.")

    # create the token
    identityToken = generate_identity_token(user_id, nonce)

    # return our token with a JSON Content-Type
    return JsonResponse({'identity_token': identityToken})

@csrf_exempt
def save_login_data(request):
    token = request.POST.get('idtoken')
    try:
        idinfo = client.verify_id_token(token, 'google_id_here')
    except crypt.AppIdentityError:
        return HttpResponse("something's wrong")
    userid = idinfo['sub']

    #set up header
    headers = {'Accept':'application/vnd.layer+json; version=1.0'}

    #retrieve layer nonce
    n = requests.post('https://api.layer.com/nonces', headers=headers)
    dic = json.loads(n.text)
    nonce = dic['nonce']

    #retrieve authentication
    url = "https://boiling-oasis-4564.herokuapp.com/get_layer_ID_token/"
    payload = {'nonce':nonce, 'user_id':userid}
    r = requests.post(url, data=payload)
    dic = json.loads(r.text)
    auth_id = str(dic['identity_token'])

    #create a personal session 
    data = {"identity_token": auth_id, "app_id": "layer_app_id_here"}
    r = requests.post('https://api.layer.com/sessions', headers=headers, json=data)
    rdic = json.loads(r.text)

    #Now to get a secure all seeing key:
    #first a nonce:
    n2 = requests.post('https://api.layer.com/nonces', headers=headers)
    dic = json.loads(n2.text)
    nonce2 = dic['nonce']
    #send to get authentication:
    payload = {'nonce':nonce2, 'user_id':"0717"}
    q = requests.post(url, data=payload)
    dic = json.loads(q.text)
    supremeId = str(dic['identity_token'])
    #create a session
    data = {"identity_token": supremeId, "app_id": "layer_app_id_here"}
    s =  requests.post('https://api.layer.com/sessions', headers=headers, json=data)
    sdic = json.loads(s.text)
    name=request.POST.get('name').rpartition(' ')
    email=request.POST.get('email').rpartition('@')
    if email[2] !='students.claremontmckenna.edu':
        return HttpResponse("/goaway")

    #Save all the data
    request.session['oauth_token']=token
    request.session['first']=name[0]
    request.session['last']=name[2]
    request.session['full']=name[0]+" " +name[2]
    request.session['email']=request.POST.get('email')
    pic = request.POST.get('pic')
    if pic is None:
        pic = "https://c2.staticflickr.com/6/5122/5281085848_dceaed6ffc.jpg"
    request.session['profpic']=pic
    request.session['id']=userid
    request.session['layer_sessionid']=rdic['session_token']
    request.session['super_key']=sdic['session_token']
    try:
        not_first = User.objects.get(pk=userid)
        return HttpResponse('/app')
    except:
        return HttpResponse('/first_login')

#Start a new conversation
@csrf_exempt
def new_convo(request):
    layerAuth = 'Layer session-token='+request.session['layer_sessionid']
    lHeaders = {'Accept':'application/vnd.layer+json; version=1.0', 'Authorization': layerAuth, "Content-Type": "application/json"}
    payload = {"participants":[request.session['id'],'0717'], "distinct": False, 'metadata':{"message":request.POST.get('message'), "description":request.POST.get('description')}}
    r = requests.post('https://api.layer.com/conversations', headers=lHeaders, json=payload)
    rdic= json.loads(r.text)
    return HttpResponse(r.text)

#Depreciated - view new converation
def join_convo(request):
    layerAuth = 'Layer session-token='+request.session['super_key']
    lHeaders = {'Accept':'application/vnd.layer+json; version=1.0', 'Authorization': layerAuth}
    r = requests.get('https://api.layer.com/conversations', headers=lHeaders)
    rdic = json.loads(r.text)
    template = 'joinconvo.html'
    c = {'convolist':rdic}

    return render(request, template, c)

@csrf_exempt
def displayConvo(request):
    
    #Set up headers and get all current parts of conversation
    url = request.POST.get('url')
    layerAuth = 'Layer session-token='+request.session['super_key']
    headers = {'Accept':'application/vnd.layer+json; version=1.0', 'Authorization': layerAuth}
    r = requests.get(url, headers = headers)
    detes = json.loads(r.text)
    #Set default of not in conversation
    inConvo = 'no'

    #Check to see if there's actually anything in the conversation... if not why bother?
    if bool(detes)==False:
        return JsonResponse({'convo':'No messages yet!', 'inConvo':inConvo})

    #Get the full list of current participants (to check in next step if current user is one)
    headers2 = {'Accept':'application/vnd.layer+json; version=1.0', 'Authorization': layerAuth}
    convoUrl = detes[0]['conversation']['url']
    q = requests.get(convoUrl, headers=headers2)
    partiDic=json.loads(q.text)
    participants=partiDic['participants']

    #check to see if the current user is part of conversation
    if request.session['id']in participants:
        inConvo='yes'

    #Put all the messages in a line by line format and save it as a string
    dastring = ""
    count = 10
    while (count>-1):
        try:
            name = User.objects.get(pk=detes[count]['sender']['user_id'])
            dastring = dastring + "<p>"+ name.full() + ": " + str(detes[count]['parts'][0]["body"])+ "</p>"
            count = count -1
        except IndexError:
            count = count - 1
    print 'here2'
    #Send it back as json
    return JsonResponse({'convo':dastring, 'inConvo':inConvo})


