from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^users/all.json$', views.all_json),
	url(r'^users/all.html$', views.all_html),
	url(r'^users/find$', views.find),
	url(r'^register$', views.register),
	url(r'^users/create$', views.create),
]