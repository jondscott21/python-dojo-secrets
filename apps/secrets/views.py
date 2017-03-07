from django.shortcuts import render, redirect, HttpResponse
from .models import User, Secret
from django.contrib import messages
from django.db.models import Count

# Create your views here.
def index(req):
	if "id" in req.session:
		return redirect('/secrets')
	return render(req, 'secrets/index.html')

def regprocess(req):
	if req.method == 'GET':
		return redirect('/')
	if req.method == 'POST':
		if User.objects.validate(req.POST)[0]:
			userid = User.objects.filter(firstname=req.POST['firstname'])[0].id
			req.session['id'] = userid
			return redirect('/secrets')
		else:
			error_messages = User.objects.validate(req.POST)[1]
			for message in error_messages:
				messages.error(req, message)
			return redirect('/')

def loginprocess(req):
	if req.method == 'GET':
		return redirect('/')
	if req.method == 'POST':
		if User.objects.login(req.POST)[0]:
			userid = User.objects.filter(email=req.POST['emaillogin'])[0].id
			req.session['id'] = userid
			return redirect('/secrets')
		else:
			error_messages = User.objects.login(req.POST)[1]
			for message in error_messages:
				messages.error(req, message)
			return redirect('/')

def secrets(req):
	if "id" not in req.session:
		return redirect('/')
	else:
		context = {
			"everyone_else": User.objects.exclude(id=req.session['id']),
			"secrets": Secret.objects.annotate(num_likes=Count('likes')).order_by('-created_at'),
			"user": User.objects.get(id=req.session['id'])
		}
		return render(req, 'secrets/secrets.html', context)

def secretprocess(req):
	if req.method == 'POST':
		if Secret.objects.display(req.POST)[0]:
			user = User.objects.get(id=req.session['id'])
			creation = Secret.objects.create(comment=req.POST['secret'], user=user)
			return redirect('/secrets')
		else:
			error_messages = Secret.objects.display(req.POST)[1]
			messages.error(req, error_messages)
			return redirect('/secrets')

def logout(req):
	try:
		del req.session['id']
	except KeyError:
		pass
	return redirect('/')

def delete(req):
	if req.method == 'POST':
		Secret.objects.filter(id=req.POST['deleteid']).delete()
		return redirect('/secrets')

def likes(req):
	if req.method == 'POST':
		user = User.objects.get(id=req.session['id'])
		secret = Secret.objects.get(id=req.POST['likeid'])
		secret.likes.add(user)
		return redirect('/secrets')

def popular(req):
	return render(req, 'secrets/popular.html')

def reroute(req):
	return HttpResponse("invalid page")