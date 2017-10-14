from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from user.models import baseUser, userSettings, publisherSettings, Event, Category, userCategory, EventCategory
from django.views.decorators.csrf import csrf_exempt
from django import forms
import json
from django.core import serializers

# Create your views here.

@csrf_exempt
def login(request):
	if(request.method != 'POST'):
		return redirect('/index.html')

	# Should clean/validate data here
	post = request.POST
	query = baseUser.objects.filter(profileId=post['profileId'])

	if(len(query)==0):
		# First Time User 
		user = baseUser(name=post['name'], email=post['email'], profileId=post['profileId'], imageUrl=post['imageUrl'])
		user.save()
		request.session['profileId'] = user.profileId
		request.session['isVerifiedPublisher']='false'
		print(request.session['profileId'])
		return JsonResponse({ 'url': '/signUp.html'})
	else:
		# Old User
		request.session['profileId'] = query.first().profileId
		print(request.session['profileId'])
		if(query.first().userType=='user'):
			return JsonResponse({ 'url': '/user.html'})
		elif(query.first().userType=='publisher'):
			request.session['isVerifiedPublisher']=publisherSettings.objects.get(profileId=request.session['profileId']).verifiedPublisher
			if(request.session['isVerifiedPublisher']=='true'):
				return JsonResponse({'url' : '/publisher.html'})
			else:
				return JsonResponse({'url':'/publisherVerification.html'})
		return HttpResponse(status=500)

@csrf_exempt
def signUp(request):
	if(request.method != 'POST'):
		return redirect('/index.html')
	post = request.POST
	profile = request.session['profileId']
	#user = baseUser(profileId=profile,userType=post['userType'])
	#user.save()
	user=baseUser.objects.get(profileId=profile)
	user.userType=post['userType']
	user.save()
	if(post['userType']=="user"):
		return JsonResponse({'url':'/userSettings.html'})
	elif(post['userType']=="publisher"):
		return JsonResponse({'url':'/publisherSettings.html'})
	else:
		return HttpResponse(status=500)

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

@csrf_exempt
def newEvent(request):
	if(request.method!='POST'):
		return redirect('/index.html')
	post=request.POST
	profile=request.session['profileId']
	authenticated=request.session['isVerifiedPublisher']
	user=baseUser.objects.get(profileId=profile)
	print(post)
	if(authenticated=='true'):
		#Using Start Time end Time. see format of Django
		eventData= Event(name=post['eventName'], categoryId=Category.objects.get(id=post['selectedCategory']), location=post['location'], description=post['description'], url=post['eventPage'], profileId=user)
		eventData.save()
		return redirect('/publisher.html')
	elif(authenticated=='false'):
		return request('/publisherVerification.html')
	return HttpResponse(status=500)

def getAllCategories(request):
	return HttpResponse(status=500)
	#No purpose for this function at the moment. Created keeping modularity in view for further working.

def getCategories(request):
	if(request.method=='GET'):
		categoryJson = serializers.serialize("json", Category.objects.all())
		data = {"categoryJson" : categoryJson}
		print(data)
		return JsonResponse(data)
	# Identify user using request.session['profileId']
	# Return array of all categories having boolean to show if user is interested or not.
	# eg Response [{ name: 'Coding', interested: true }, { name: 'Robotics', interested: false }]
	#return HttpResponse("Hello World. You're at the poll index. GETCATEGORIES")
def saveCategories(request):
	# Identify user using request.session['profileId']
	# Accept data in this format Response [{ name: 'Coding', interested: true }, { name: 'Robotics', interested: false }]
	return HttpResponse("Hello World. You're at the poll index. SAVECATEGORIES")
def getSettings(request):
	return HttpResponse("Hello World. You're at the poll index. GETSETTINGS")

#Change the method to edit settings. at the moment it works on delete save

#Use functions to decrease repeatation of code. E.g saveCategories
@csrf_exempt
def saveSettings(request):
	if(request.method != 'POST'):
		return redirect('/index.html')
	post = request.POST
	profile = request.session['profileId']
	baseUserData = baseUser.objects.get(profileId=profile)
	selected = dict(post)
	print(selected)
	if(baseUserData.userType=='user'):
		if(userSettings.objects.filter(profileId=baseUserData)):
			user=userSettings.objects.get(profileId=profile)
			user.delete()
			user=userSettings(profileId=baseUser.objects.get(profileId=profile),rollNumber=post['rollNumber'],department=post['department'])
			user.save()
			for i in range (0,len(selected['selectedCategory'])):
				categoryData=Category.objects.get(id=selected['selectedCategory'][i])
				form=userCategory(userId=baseUserData,categoryId=categoryData)
				form.save()
			return redirect('/user.html')
		else:
			user=userSettings(profileId=baseUser.objects.get(profileId=profile),rollNumber=post['rollNumber'],department=post['department'])
			user.save()
			for i in range (0,len(selected['selectedCategory'])):
				categoryData=Category.objects.get(id=str(i))
				form=userCategory(userId=baseUserData,categoryId=categoryData)
				form.save()
			return redirect('/user.html')
	elif(baseUserData.userType=="publisher"):
		if(publisherSettings.objects.filter(profileId=baseUserData)):
			user=publisherSettings.objects.get(profileId=profile)
			user.delete()
			user=publisherSettings(profileId=baseUser.objects.get(profileId=profile),displayName=post['Alias'],website=post['website'], contactNumber=post['contactNumber'])
			user.save()
			if(user.verifiedPublisher=='true'):
				return redirect('/publisher.html')
			else:
				return redirect('/publisherVerification.html')
		else:
			user=publisherSettings(profileId=baseUser.objects.get(profileId=profile),displayName=post['Alias'],website=post['website'], contactNumber=post['contactNumber'])
			user.save()
			if(user.verifiedPublisher=='true'):
				return redirect('/publisher.html')
			else:
				return redirect('/publisherVerification.html')
	return HttpResponse(status=500)


@csrf_exempt
def getEvents(request):
	# Identify user using request.session['profileId']
	# Return array of events relevant to that user.
	profile=request.session['profileId']
	post=request.POST
	baseUserData=baseUser.objects.get(profileId=profile)
	if(baseUserData.userType=='publisher'):
		eventsJson = serializers.serialize("json", Event.objects.filter(profileId=baseUserData))
		data = {"eventsJson" : eventsJson}
		print(data)
		return JsonResponse(data)
	elif(baseUserData.userType=='user'):
		categoryJson = serializers.serialize("json", userCategory.objects.filter(userId=baseUserData))
		categoryData = {"categoryJson" : categoryJson}
		print(categoryData)
		userCategoryData=Category.objects.filter(id__in=categoryDatafields.categoryId)
		print(userCategoryData)
		eventsJson = serializers.serialize("json", Event.objects.filter(categoryId__in=userCategoryData))
		data = {"eventsJson" : eventsJson}
		print(data)
		return JsonResponse(data)
		#return JsonResponse({'data': [{'name': 'Programming Contest','start_time': '1506686400','end_time': '1506688400','location': 'Hall 5, IIT Kanpur','description': 'Online hackathon. 5 member teams.','publishedBy': 'Programming CLub'},{'name': 'Programming Contest','start_time': '1506686400','end_time': '1506688400','location': 'Hall 5, IIT Kanpur','description': 'Online hackathon. 5 member teams.','publishedBy': 'Programming CLub'},{'name': 'Programming Contest','start_time': '1506686400','end_time': '1506688400','location': 'Hall 5, IIT Kanpur','description': 'Online hackathon. 5 member teams.','publishedBy': 'Programming CLub'},{'name': 'Programming Contest','start_time': '1506686400','end_time': '1506688400','location': 'Hall 5, IIT Kanpur','description': 'Online hackathon. 5 member teams.','publishedBy': 'Programming CLub'},{'name': 'Programming Contest','start_time': '1506686400','end_time': '1506688400','location': 'Hall 5, IIT Kanpur','description': 'Online hackathon. 5 member teams.','publishedBy': 'Programming CLub'}]})


#Edits in the future
#Only certain fields can be serialized