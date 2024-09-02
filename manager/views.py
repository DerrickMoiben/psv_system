from django.shortcuts import render
from django.http import HttpResponse
from forms import ManagerLoginForm, ManagerSingupForm
from django.contrib.auth.models import User



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
                user = User.objects.create_user(username, email, password)
                user.save()
                return HttpResponse('User created successfully')
            else:
                return HttpResponse('Password does not match')
    else:
        form = ManagerSingupForm()
    return render(request, 'signup.html', {'form': form})
