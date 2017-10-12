from django.db import models

# Create your models here.

class baseUser(models.Model):
    name 		= models.CharField(max_length=200)
    email 		= models.CharField(max_length=200)
    profileId 	= models.CharField(max_length=200, primary_key=True)
    imageUrl 	= models.CharField(max_length=200)
    userType	= models.CharField(max_length=200)

    
    def __str__(self):
        return self.name + '-' + self.email + '-' + self.profileId + '-' + self.imageUrl

class userSettings(models.Model):
	profileId	=models.ForeignKey(baseUser, on_delete=models.CASCADE)
	rollNumber	=models.CharField(max_length=6)
	department	=models.CharField(max_length=50)

	def __str__(self):
		return self.profileId + '-' + self.rollNumber + '-' + self.department

class publisherSettings(models.Model):
	profileId	= models.ForeignKey(baseUser, on_delete=models.CASCADE)
	displayName	= models.CharField(max_length=100)
	website		= models.CharField(max_length=100)
	contentType	= models.CharField(max_length=100)
	verifiedPublisher = models.CharField(max_length=5, default='false')
	contactNumber =models.CharField(max_length=10, default='')

	def __str__(self):
		return self.profileId.profileId + '-' + self.displayName + '-' + self.website + '-' + self.contentType

class Event(models.Model):
	name 			= models.CharField(max_length=200,default='')
	start_time 		= models.DateTimeField(default='1999-05-31 12:00')
	end_time 		= models.DateTimeField(default='1999-05-31 12:00') 
	location 		= models.CharField(max_length=200,default='')
	description 	= models.CharField(max_length=500, default='')
	url				= models.CharField(max_length=100, default='')
	profileId	 	= models.ForeignKey(baseUser, on_delete=models.CASCADE, default='')

	def __str__(self):
		return self.name + '-' +self.url + '-' + self.location + '-' + self.description + '-' +self.profileId.profileId

class Category(models.Model):
	name 		= models.CharField(max_length=200)

class UserCategory(models.Model):
	userId 		= models.ForeignKey(baseUser, on_delete=models.CASCADE)
	categoryId 	= models.ForeignKey(Category, on_delete=models.CASCADE)

class EventCategory(models.Model):
	eventId 	= models.ForeignKey(Event, on_delete=models.CASCADE)
	categoryId 	= models.ForeignKey(Category, on_delete=models.CASCADE)