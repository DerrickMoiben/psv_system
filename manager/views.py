# This file contains the views for the manager app  
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ManagerLoginForm, ManagerSingupForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required




"""This is a fuction for the manager to sign up then login"""
def manager_signup(request):
    if request.method == 'POST':
        form = ManagerSingupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            fullname = form.cleaned_data['fullname']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            if password == password2:
                try:
                    user = User.objects.create_user(username,  fullname, email, password)
                    user.save()
                    messages.sucess(request, 'Account created successfully')
                    return redirect('manager_login')
                except Exception as e:
                    messages.error(request, 'An error occured {}' .format(e))
            else:
                messages.error(request, 'Passwords do not match')          
    else:
        form = ManagerSingupForm()
    return render(request, 'signup.html', {'form': form})

def manager_login(request):
    if request.method == 'POST':
        form = ManagerLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('manager_dashboard')
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = ManagerLoginForm()
    return render(request, 'login.html', {'form': form})



@login_required
def manager_dashboard(request):
    return render(request, 'dashboard.html')