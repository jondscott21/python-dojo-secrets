from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

# Create your models here.
class UserManager(models.Manager):
	def validate(self, postData):
		messages = []
		email_pattern = re.compile('^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
		name_pattern = re.compile('^[a-zA-Z]{2,}$')
		pw_pattern = re.compile('^[\w\W]{8,}$')
		if len(postData['firstname']) > 1 and name_pattern.match(postData['firstname']): 
			pass
		else:
			messages.append('first name is invalid')
		if len(postData['lastname']) > 1 and name_pattern.match(postData['lastname']):
			pass
		else:
			messages.append('last name is invalid')
		if email_pattern.match(postData['email']):
			if len(User.objects.filter(email=postData['email'])) > 0:
				messages.append('Email already exists')
			else:
				pass
		else:
			messages.append('email pattern is invalid')
		if len(postData['pwreg']) > 7 and pw_pattern.match(postData['pwreg']):
			if postData['pwreg'] == postData['confirmpw']:
				pass
			else:
				messages.append('password did not match confirmation')
		else:
			messages.append('password did not match requirements')
		if messages:
			return (False, messages)
		else:
			password = postData['pwreg']
			hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).encode()
			User.objects.create(firstname=postData['firstname'], lastname=postData['lastname'], email=postData['email'], password=hashed)
			return (True, "I'm a troll")

	def login(self, postData):
		messages = []
		try:
			User.objects.get(email=postData['emaillogin'])
		except:
			messages.append("Email doesn't exist")
			return (False, messages)	
				#run above line to check if email exists in database already 
		emails = User.objects.filter(email=postData['emaillogin'])[0]
		if postData['emaillogin'] == emails.email:
			password = postData['pwlogin']
			existing_pw = emails.password
			if bcrypt.hashpw(password.encode(), existing_pw.encode()) == existing_pw:
				return (True, "Still trollin'")
			else:
				messages.append("Incorrect password")
		return (False, messages)

class SecretManager(models.Manager):
	def display(self, postData):
		if len(postData['secret']) > 0:
			return (True, "blah blah")
		else:
			return (False, "Need greater than 1 character")

class User(models.Model):
	firstname = models.CharField(max_length=255)
	lastname = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()	

class Secret(models.Model):
	comment = models.CharField(max_length=140)
	user = models.ForeignKey(User, related_name='secrets')
	likes = models.ManyToManyField(User, related_name='user_likers')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = SecretManager()

