from __future__ import unicode_literals
from .models import User, Task
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.db.models import Sum
from datetime import date
import time

def index(request):
	context={
		'users': User.objects.all()
	}
	return render(request, "login_reg/index.html", context)

def registration(request):
	result = User.objects.validate_registration(request.POST)	
	if type(result) == list:
		for err in result:
			messages.error(request, err)
		return redirect('/')
	request.session['user_id'] = result.id
	messages.success(request, "Registration Successful!")
	return redirect('/appointments')

def login(request):
	result = User.objects.validate_login(request.POST)
	if type(result) == list:
		for err in result:
			messages.error(request, err)
		return redirect('/')
	request.session['user_id'] = result.id
	messages.success(request, "Login Successful!")
	return redirect('/appointments')

def appointments(request):
	if 'user_id' not in request.session:
		return redirect('/')
	current_user = User.objects.get(id = request.session['user_id'])
	current_date = date.today()

	context = {
		'current_user': current_user,
		'tasks':Task.objects.all(),
		'today_schedule':Task.objects.filter(created_by=current_user, date=current_date),
		'other_tasks':Task.objects.filter(created_by=current_user).exclude(date=current_date)
	}	
	return render(request, 'login_reg/appointments.html', context)

def add(request):
	if 'user_id' not in request.session:
		return redirect('/')
	current_user = User.objects.get(id = request.session['user_id'])
	Task.objects.create(
		date=request.POST['date'],
		time=request.POST['time'],
		task_name=request.POST['task_name'],
		created_by=current_user,
		status='pending'
		)
	return redirect('/appointments')

def edit(request, task_id):
	if 'user_id' not in request.session:
		return redirect('/')
	current_user = User.objects.get(id = request.session['user_id'])

	context = {
		'current_user':current_user,
		'tasks':Task.objects.get(id = task_id),
		'task_name':Task.objects.get(id = task_id).task_name,
		'status':Task.objects.get(id = task_id).status,
		'date':Task.objects.get(id = task_id).date,
		'time':Task.objects.get(id = task_id).time
		}
	return render(request, "login_reg/edit.html", context)

def update(request, task_id):
	print request.POST
	print "TASK UPDATE ROUTE"
	if 'user_id' not in request.session:
		return redirect('/')
	current_user = User.objects.get(id = request.session['user_id'])
	t = Task.objects.get(id=task_id)
	t.task_name = request.POST['task_name']
	t.status = request.POST['status']
	t.date = request.POST['date']
	t.time = request.POST['time']
	t.save()

	return redirect('/appointments')


def delete(request, task_id):
	t = Task.objects.get(id = task_id)
	t.delete()
	return redirect('/appointments')

def logout(request, user_id):
	del request.session
	return redirect('/')
