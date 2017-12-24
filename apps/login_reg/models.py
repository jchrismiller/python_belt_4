from __future__ import unicode_literals
import re
import bcrypt
from django.db import models
from datetime import date
import time

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')

class UserManager(models.Manager):
	def validate_login(self, post_data):
		errors = []
		# check DB for post_data['email']
		print post_data
		if len(self.filter(email=post_data['email'])) > 0:
			# check this user's password
			user = self.filter(email=post_data['email'])[0]
			if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
				errors.append('email/password incorrect')
		else:
			errors.append('email/password incorrect')

		if errors:
			return errors
		return user

	def validate_registration(self, post_data):
		errors = []
		# check length of name fields
		if len(post_data['name']) < 2:
			errors.append("name fields must be at least 3 characters")
		# check length of name password
		if len(post_data['password']) <8:
			errors.append("password must be at least 8 characters")
		# check name fields for letter characters
		if not re.match(NAME_REGEX, post_data['name']):
			errors.append("name fields must be letter characters only")
		# check emailness of email
		if not re.match(EMAIL_REGEX, post_data['email']):
			errors.append("invalid email")
		# check uniquness of email
		if len(User.objects.filter(email=post_data['email'])) > 0:
			errors.append("email already in use")
		# check password == password confirm
		if post_data['password'] != post_data['confirm_password']:
			errors.append("passwords do not match")

		# if post_data['robot'] != post_data['True']:
		# 	errors.append("No robots allowed!")

		if not errors:
			# make our new user
			# hash password
			hashed = bcrypt.hashpw((post_data['password'].encode()), bcrypt.gensalt(5))

			new_user = self.create(
				name=post_data['name'],
				email=post_data['email'],
				password = hashed,
				dob = post_data['dob']
			)
			return new_user
		return errors

class TaskManager(models.Manager):
	def validate(self, post_data):
		pass
		# no empty entries
		# travel dates should be future-dated
		# start should be before end
		new_task = self.create(
			task_name=post_data['task_name'],
			status='pending',
			date=post_data['date'],
			time=post_data['time'],
			created_by=user
				)
		return new_travel		

class User(models.Model):
	name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	dob = models.DateField(blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

	objects = UserManager()

	def __repr__(self):
		return "<User: {} {} {} {} {}>".format(self.id, self.name, self.email, self.dob)

class Task(models.Model):
	task_name = models.CharField(max_length=255)
	status = models.CharField(max_length=255)
	date = models.DateField(blank=True, null=True)
	time = models.TimeField(blank=True, null=True)
	created_by = models.ForeignKey(User, related_name = 'appointments')
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

