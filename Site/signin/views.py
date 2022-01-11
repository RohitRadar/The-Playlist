from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate , logout
from django.contrib import messages

def signin(request):
	if request.method == "POST" :
		form = AuthenticationForm(request=request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username,password=password)
			if user is not None:
				login(request, user)
				return redirect('signin/')
		else:
			messages.error(request,"invalid Username or Password")
	form = AuthenticationForm()	
	return render(request,'signin.html', {'form':form})

def signout(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect('signin/')