from django.db import models

# Create your models here.

class User(models.Model):
    name 		= models.CharField(max_length=200)
    email 		= models.CharField(max_length=200)
    profileId 	= models.CharField(max_length=200)
    imageUrl 	= models.CharField(max_length=200)
    rollNumber 	= models.CharField(max_length=200)
    department 	= models.CharField(max_length=200)
    
    def __str__(self):
        return self.name + '-' + self.email + '-' + self.profileId + '-' + self.imageUrl

class Event(models.Model):
	name 			= models.CharField(max_length=200)
	start_time 		= models.DateTimeField()
	end_time 		= models.DateTimeField() 
	location 		= models.CharField(max_length=200)
	description 	= models.CharField(max_length=500)
	publisher_id 	= models.CharField(max_length=200)

	def __str__(self):
		return self.name + '-' +self.time + '-' + self.location + '-' + self.description + '-' +self.publisher_id

class Category(models.Model):
	name 		= models.CharField(max_length=200)

class UserCategory(models.Model):
	userId 		= models.ForeignKey(User, on_delete=models.CASCADE)
	categoryId 	= models.ForeignKey(Category, on_delete=models.CASCADE)

class EventCategory(models.Model):
	eventId 	= models.ForeignKey(Event, on_delete=models.CASCADE)
	categoryId 	= models.ForeignKey(Category, on_delete=models.CASCADE)