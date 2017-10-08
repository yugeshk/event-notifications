from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'login',views.login, name='login'),
	url(r'logout',views.logout, name='logout'),
	url(r'isLoggedIn', views.isLoggedIn, name='isLoggedIn'),
	url(r'getCategories', views.getCategories, name='getCategories'),
	url(r'saveCategories', views.saveCategories, name='saveCategories'),
	url(r'getSettings', views.getSettings, name='getSettings'),
	url(r'saveSettings', views.saveSettings, name='saveSettings'),
	url(r'getEvents', views.getEvents, name='getEvents'),
	url(r'signUp', views.signUp, name='signUp')	
]