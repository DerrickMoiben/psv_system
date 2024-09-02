# This file contains the views for the manager app  
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ManagerLoginForm, ManagerSingupForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect




"""This is a fuction for the manager to sign up then login"""
@csrf_protect
def manager_signup(request):
    if request.method == 'POST':
        form = ManagerSingupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')
            return redirect('manager_login')
        else:
            messages.error(request, 'An error occurred during registration' )
            print(form.errors)
            
    else:
        form = ManagerSingupForm()
    return render(request, 'signup.html', {'form': form})

@csrf_protect
def manager_login(request):
    if request.method == 'POST':
        form = ManagerLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful')
                return redirect('manager_dashboard')
            else:
                messages.error(request, 'Invalid username or password')
                form.errors()
    else:
        form = ManagerLoginForm()
    return render(request, 'login.html', {'form': form})



@login_required
def manager_dashboard(request):
    return render(request, 'dashboard.html')