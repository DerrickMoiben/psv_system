from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from .forms import CashierSignupForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseForbidden

# Create your views here.\

def index(request):
    return render(request, 'index.html')


def cashier_dashboard(request):
    if request.user.role not in ['manager', 'cashier']:
        return HttpResponseForbidden("You do not have permission to view this page.")
    return render(request, 'cashier_dashboard.html')

@csrf_protect
def cashier_signup(request):
    if request.method == 'POST':
        form = CashierSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'cashier'  # Set role as cashier
            user.save()
            messages.success(request, 'Cashier account created successfully')
            return redirect('cashier_login')
        else:
            messages.error(request, 'An error occurred during registration')
            print(form.errors)
            
    else:
        form = CashierSignupForm()
    return render(request, 'signupcashier.html', {'form': form})


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def cashier_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Allow both cashiers and managers to access the cashier dashboard
            if user.role == 'cashier' or user.role == 'manager':
                login(request, user)
                return redirect('cashier_dashboard')  # Redirect to cashier dashboard
            else:
                return render(request, 'cashier_login.html', {'errors': 'You are not authorized to access the cashier dashboard'})
        else:
            return render(request, 'cashier_login.html', {'errors': 'Invalid credentials'})

    return render(request, 'cashier_login.html')
