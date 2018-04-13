# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

from django.db import models
import datetime
from datetime import date
import bcrypt
import re
EMAIL_REGEX=re.compile(r'^[a-zA-Z0-9+._-]+@[a-zA-Z0-9+._-]+\.[a-zA-Z]+$')
NAME_REGEX=re.compile(r'^[A-Za-z]\w+$')

# Create your models here.
class UserManager(models.Manager):
	def reg_validator(self, postData):
		errors = {}
		if len(postData['first_name'])< 2:
			errors['first_name'] = "Invalid first name. Min 2 characters."
		elif not re.match(NAME_REGEX, postData['first_name']):
			errors['first_name'] = "Invalid entry. Must only contain letters."
		if len(postData['last_name'])< 2:
			errors['last_name'] = "Invalid last name. Min 2 characters."
		elif not re.match(NAME_REGEX, postData['last_name']):
			errors['last_name'] = "Invalid entry. Must only contain letters."

		if len(postData['birthdate'])< 0 or len(postData['birthdate']) == "":
			errors['birthdate'] = "Please enter a birthdate."

		try: 
			postData['birthdate']
			birthdate = datetime.datetime.strptime(postData['birthdate'], "%m-%d-%Y")
			today = datetime.date.today()
			today_ref = datetime.datetime(today.month, today.day, today.year)

			if birthdate > today_ref:
				errors['birthdate'] = "Invalid birthdate. Please try again."

		except:
			pass

		try: 
			postData['birthdate']
			birthdate = datetime.datetime.strptime(postData['birthdate'], "%m-%d-%Y")
			today = datetime.date.today()
			today_ref = datetime.datetime(today.month, today.day, today.year)

			if (today_ref - birthdate) < 21:
				errors['birthdate'] = "Sorry. You must be 21 and over to register."

		except:
			pass
		# if len(postData['birthdate'])>datetime.datetime.strptime(postData['birthdate'], "%m-%d-%Y").today.date():
		# 	errors['birthdate'] = "Invalid birthdate. Please try again."
		# if (datetime.datetime.now()-datetime.datetime.strptime(birthdate=postData['birthdate']), "%m-%d-%Y")< 21:
		# 	errors['birthdate'] = "Sorry. You must be 21 and over to register."

		if len(postData['email'])< 1:
			errors['email'] = "Must enter an email."
		elif len(User.objects.filter(email=postData['email']))> 0:
			errors['email'] = "Email already in use."
		elif not re.match(EMAIL_REGEX, postData['email']):
			errors['email'] = "Invalid email. Please try again."

		if len(postData['password'])< 8:
			errors['password'] = "Password must be at least 8 characters."
		elif postData['password']!= postData['confirm']:
			errors['password'] = "Password confirmation did not match."
		return errors

	def new_user(self, postData):
		user = User.objects.create(
			first_name=postData['first_name'],
			last_name=postData['last_name'],
			email=postData['email'],
			birthdate=postData['birthdate'],
			password=bcrypt.hashpw(postData['password'].encode(),bcrypt.gensalt(5)),
		)
		return user

	def login_validator(self, postData):
		errors = {}
		try:
			user = User.objects.get(email=postData['email'])
			if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
				errors['login_error']="Invalid email/password."
		except:
			errors['login_error'] = "Invalid login."
		if errors:
			return errors
		return user

class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	birthdate = models.DateField(auto_now_add=False, auto_now=False)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

	objects = UserManager()