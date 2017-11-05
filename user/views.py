from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from user.models import baseUser, userSettings, publisherSettings, Event, Category, userCategory, EventCategory
from django.views.decorators.csrf import csrf_exempt
from django import forms
import json
from django.core import serializers
import datetime
from oauth2client import client, GOOGLE_TOKEN_URI

# Importing Google Libraries
import google.oauth2.credentials
import google_auth_oauthlib.flow
import httplib2
from googleapiclient.discovery import build

CLIENT_ID = "403176586402-2573bsbcg6ltedsgra1s5lgs5065mbuk.apps.googleusercontent.com"
CLIENT_SECRET = "f_kT9oFHKr0REkUpYPbTLVAm"

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
		flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('client_secret.json', scopes=['https://www.googleapis.com/auth/calendar'])
		flow.redirect_uri = 'http://localhost:8000/user/handleGoogleResponse'
		authorization_url, state = flow.authorization_url(access_type='offline',include_granted_scopes='true',state='yugesh')
		request.session['state'] = state
		return JsonResponse({ 'url': authorization_url})
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
		startTime = datetime.datetime.strptime(post['startDate']+' '+post['startTime'],'%m/%d/%Y %H:%M')
		endTime = datetime.datetime.strptime(post['endDate']+' '+post['endTime'],'%m/%d/%Y %H:%M')
		eventData = Event(name=post['eventName'], categoryId=Category.objects.get(id=post['selectedCategory']), location=post['location'], description=post['description'], url=post['eventPage'], profileId=user, start_time=startTime, end_time=endTime)
		eventData.save()

		#Calling Google APIs
		pushToUsers = userCategory.objects.filter(categoryId=post['selectedCategory']).values('userId')
		print(pushToUsers)
		for i in range (0,len(pushToUsers)):
			userToPush=baseUser.objects.get(profileId=pushToUsers[i]['userId'])
			credentials = google.oauth2.credentials.Credentials(token=None, refresh_token=userToPush.googleCode, id_token=None, client_secret='f_kT9oFHKr0REkUpYPbTLVAm', client_id='403176586402-2573bsbcg6ltedsgra1s5lgs5065mbuk.apps.googleusercontent.com', token_uri='https://accounts.google.com/o/oauth2/token', scopes=['https://www.googleapis.com/auth/calendar'])
			event = {
				'summary': post['eventName'],
				'location': post['location'],
				'description': post['description'],
				'start': {
					'dateTime': startTime.strftime("%Y-%m-%dT%H:%M:00+05:30"),
					'timeZone': 'Asia/Kolkata',
				},
				'end': {
					'dateTime': endTime.strftime("%Y-%m-%dT%H:%M:00+05:30"),
					'timeZone': 'Asia/Kolkata',
				},
				'reminders': {
					'useDefault': False,
					'overrides': [
						{'method': 'email', 'minutes': 24 * 60},
						{'method': 'popup', 'minutes': 30},
					],
				},
			}
			service = build('calendar', 'v3', credentials=credentials)
			event = service.events().insert(calendarId='primary', body=event).execute()
			print('Event created: %s' % (event.get('htmlLink')))
		return redirect('/publisher.html')
	elif(authenticated=='false'):
		return request('/publisherVerification.html')

	#Google Api Code
	# state = 'yugesh'
	# flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('client_secret.json',scopes=['https://www.googleapis.com/auth/calendar'],state=state)
	# flow.redirect_uri = 'http://localhost:8000/user/handleGoogleResponse'
	# flow.fetch_token(code='4/pOT7BRCD1UDaL_Lhyphd3S4kaSH4eSbRj4pVOkoiA5A')
	
	# # print('token'+ flow.credentials.token)
	# # print('refresh_token'+ flow.credentials.refresh_token)
	# # print('token_uri'+ flow.credentials.token_uri)
	# # print('client_id'+ flow.credentials.client_id)
	# # print('client_secret'+ flow.credentials.client_secret)
	# # print('scopes'+ flow.credentials.scopes)
	
	# print('Received token!')
	
	# service = build('calendar', 'v3', credentials=flow.credentials)
	# event = {
	# 	'summary': 'Google I/O 2015',
	# 	'location': '800 Howard St., San Francisco, CA 94103',
	# 	'description': 'A chance to hear more about Google\'s developer products.',
	# 	'start': {
	# 		'dateTime': '2017-10-28T09:00:00-07:00',
	# 		'timeZone': 'America/Los_Angeles',
	# 	},
	# 	'end': {
	# 		'dateTime': '2017-10-29T17:00:00-07:00',
	# 		'timeZone': 'America/Los_Angeles',
	# 	},
	# 	'reminders': {
	# 		'useDefault': False,
	# 		'overrides': [
	# 			{'method': 'email', 'minutes': 24 * 60},
	# 			{'method': 'popup', 'minutes': 10},
	# 		],
	# 	},
	# }

	# event = service.events().insert(calendarId='primary', body=event).execute()
	# print('Event created: %s' % (event.get('htmlLink')))




	return HttpResponse(status=500)

def getAllCategories(request):
	return HttpResponse(status=500)
	#No purpose for this function at the moment. Created keeping modularity in view for further working.

def getCategories(request):
	if(request.method=='GET'):
		baseUserData=baseUser.objects.get(profileId=request.session['profileId'])
		if(baseUserData.userType=='user'):
			settings=userSettings.objects.get(profileId=baseUserData)
			categoryJson = serializers.serialize("json", Category.objects.all())
			data = {"categoryJson" : categoryJson, "roll" : settings.rollNumber, "dept" : settings.department }
			print(data)
			return JsonResponse(data)
		elif(baseUserData.userType=='publisher'):
			settings=publisherSettings.objects.get(profileId=baseUserData)
			categoryJson = serializers.serialize("json", Category.objects.all())
			data = {"categoryJson" : categoryJson, "name" : settings.displayName}
			print(data)
			return JsonResponse(data)
	# Identify user using request.session['profileId']
	# Return array of all categories having boolean to show if user is interested or not.
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
			userCategoryData=userCategory.objects.filter(userId=baseUserData)
			userCategoryData.delete()
			user.rollNumber=post['rollNumber']
			user.department=post['department']
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
				categoryData=Category.objects.get(id=selected['selectedCategory'][i])
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
	now=datetime.date.today()
	baseUserData=baseUser.objects.get(profileId=profile)
	if(baseUserData.userType=='publisher'):
		settings=publisherSettings.objects.get(profileId=baseUserData)
		eventsJson = serializers.serialize("json", Event.objects.filter(profileId=baseUserData, start_time__date__gte=now))
		data = {"eventsJson" : eventsJson}
		print(data)
		return JsonResponse(data)
	elif(baseUserData.userType=='user'):
		settings=userSettings.objects.get(profileId=baseUserData)
		eventData = Event.objects.raw('SELECT * FROM user_event INNER JOIN user_usercategory ON user_event.categoryId_id=user_usercategory.categoryId_id AND user_usercategory.userId_id='+'"'+request.session['profileId']+'"'+"AND user_event.start_time >= DATETIME('now')")
		print(eventData)
		eventsJson = serializers.serialize("json", eventData)
		data = {"eventsJson" : eventsJson, "name" : baseUserData.name, "roll" : settings.rollNumber, "dept" : settings.department}
		print(data)
		return JsonResponse(data)
		
@csrf_exempt
def handleGoogleResponse(request):
	print(request.GET['code'])
	print(request.GET['state'])
	profile=request.session['profileId']
	user=baseUser.objects.get(profileId=profile)
	
	## Get credentials
	state='yugesh'
	flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('client_secret.json',scopes=['https://www.googleapis.com/auth/calendar'],state=state)
	flow.redirect_uri = 'http://localhost:8000/user/handleGoogleResponse'
	flow.fetch_token(code=request.GET['code'])
	user.googleCode = flow.credentials.refresh_token
	user.save()

	return redirect('/signUp.html')

@csrf_exempt
def search(request):
	post=request.POST
	user=baseUser.objects.get(profileId=request.session['profileId'])
	startTime = datetime.datetime.strptime(post['startDate']+' '+post['startTime'],'%m/%d/%Y %H:%M')
	endTime = datetime.datetime.strptime(post['endDate']+' '+post['endTime'],'%m/%d/%Y %H:%M')
	eventData=Event.objects.filter(start_time__range=(startTime,endTime))
	eventsJson = serializers.serialize("json", eventData)
	data = {"eventsJson" : eventsJson, "name" : publisherSettings.objects.get(profileId=user).displayName}
	print(data)
	return JsonResponse(data)

@csrf_exempt
def pageData(request):
	baseUserData=baseUser.objects.get(profileId=request.session['profileId'])
	if(baseUserData.userType=='publisher'):
		settings=publisherSettings.objects.get(profileId=baseUserData)
		data={"name" : settings.displayName}
		print(data)
		return JsonResponse(data)
	elif(baseUserData.userType=='user'):
		settings=userSettings.objects.get(profileId=baseUserData)
		return JsonResponse({"name" : baseUserData.name, "roll" : settings.rollNumber, "dept" : settings.department})