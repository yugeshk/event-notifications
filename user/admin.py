from django.contrib import admin
from .models import baseUser, userSettings, publisherSettings, Event, Category, userCategory, EventCategory

admin.site.register(baseUser)
admin.site.register(userSettings)
admin.site.register(publisherSettings)
admin.site.register(Event)
admin.site.register(Category)
admin.site.register(userCategory)
admin.site.register(EventCategory)

# Register your models here.
