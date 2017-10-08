from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from user.models import User
from django.views.decorators.csrf import csrf_exempt
from django import forms
import json

# Create your views here.

@csrf_exempt
def login(request):
	if(request.method != 'POST'):
		return redirect('/index.html')

	# Should clean/validate data here
	post = request.POST
	query = User.objects.filter(profileId=post['profileId'])

	if(len(query)==0):
		# First Time User 
		user = User(name=post['name'], email=post['email'], profileId=post['profileId'], imageUrl=post['imageUrl'])
		user.save()
		request.session['profileId'] = user['profileId']
		print(request.session['profileId'])
		return JsonResponse({ 'url': '/signUp.html'})
	else:
		# Old User
		request.session['profileId'] = query.first().profileId
		print(request.session['profileId'])
		return JsonResponse({ 'url': '/user.html'})

#create a signup rather than using login for both login and signup

@csrf_exempt
def logout(request):
	if(request.method != 'POST'):
		return redirect('/index.html')
	
	request.session.flush()
	return JsonResponse({ 'url': '/index.html'})		

@csrf_exempt
def isLoggedIn(request):
	if(request.session['profileId']):
		return HttpResponse(status=200)
	else:
		return HttpResponse(status=500)

def getCategories(request):
	# Identify user using request.session['profileId']
	# Return array of all categories having boolean to show if user is interested or not.
	# eg Response [{ name: 'Coding', interested: true }, { name: 'Robotics', interested: false }]
	return HttpResponse("Hello World. You're at the poll index. GETCATEGORIES")
def saveCategories(request):
	# Identify user using request.session['profileId']
	# Accept data in this format Response [{ name: 'Coding', interested: true }, { name: 'Robotics', interested: false }]
	return HttpResponse("Hello World. You're at the poll index. SAVECATEGORIES")
def getSettings(request):
	return HttpResponse("Hello World. You're at the poll index. GETSETTINGS")
def saveSettings(request):
	return HttpResponse("Hello World. You're at the poll index. SAVESETTINGS")

@csrf_exempt
def getEvents(request):
	# Identify user using request.session['profileId']
	# Return array of events relevant to that user.
	return JsonResponse({'data': [{'name': 'Programming Contest','start_time': '1506686400','end_time': '1506688400','location': 'Hall 5, IIT Kanpur','description': 'Online hackathon. 5 member teams.','publishedBy': 'Programming CLub'},{'name': 'Programming Contest','start_time': '1506686400','end_time': '1506688400','location': 'Hall 5, IIT Kanpur','description': 'Online hackathon. 5 member teams.','publishedBy': 'Programming CLub'},{'name': 'Programming Contest','start_time': '1506686400','end_time': '1506688400','location': 'Hall 5, IIT Kanpur','description': 'Online hackathon. 5 member teams.','publishedBy': 'Programming CLub'},{'name': 'Programming Contest','start_time': '1506686400','end_time': '1506688400','location': 'Hall 5, IIT Kanpur','description': 'Online hackathon. 5 member teams.','publishedBy': 'Programming CLub'},{'name': 'Programming Contest','start_time': '1506686400','end_time': '1506688400','location': 'Hall 5, IIT Kanpur','description': 'Online hackathon. 5 member teams.','publishedBy': 'Programming CLub'}]})