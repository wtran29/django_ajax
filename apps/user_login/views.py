# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from models import *
from django.contrib import messages
from django.core import serializers
import json
# Create your views here.
def register(request):
	if request.method == "POST":
		errors = User.objects.reg_validator(request.POST)
		if len(errors):
			for tag, error in errors.iteritems():
				messages.error(request, error, extra_tags=tag)
				return redirect('/')
		else:
			user = User.objects.new_user(request.POST)
			request.session['id'] = user.id
			messages.success(request, " You are registered.")
			return redirect('/')
	return redirect('/')

def index(request):
	return render(request, 'users/index.html')

def all_json(request):
	return HttpResponse(serializers.serialize("json", User.objects.all()), content_type="application/json")

def all_html(request):
	return render(request, "users/all.html", {'users': User.objects.all()})

def find(request):
	print request.POST
	search = request.POST['search']
	return render(request, "users/all.html", { 'users': User.objects.filter(first_name__startswith = search) })

def create(request):
	print request.POST
	User.objects.create(
		first_name=request.POST['first_name'],
		last_name=request.POST['last_name'],
		email=request.POST['email'],
		birthdate=request.POST['birthdate']
		)
	return render(request, "users/all.html", {"users": User.objects.all().order_by('-created_at')})