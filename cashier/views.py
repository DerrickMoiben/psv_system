from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from .forms import CashierSignupForm, TicketForm, RouteSelectionForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseForbidden
from .models import Route, Ticket


# Create your views here.\

def index(request):
    return render(request, 'staffindex.html')


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



"""This will be used to select he route then it dynamically loads the stages for the selected route"""


def select_route(request):
    if request.method == 'POST':
        selected_route_id = request.POST.get('route')
        try:
            selected_route = Route.objects.get(pk=selected_route_id)
            
            request.session['selected_route'] = selected_route_id
            return redirect('cut_ticket')
        except Route.DoesNotExist:
            messages.error(request, 'Selected route does not exist')
            return redirect('select_route')
    else:
        form = RouteSelectionForm()
    return render(request, 'select_route.html', {'form': form})



def cut_ticket(request):
    # Retrieve selected route from session
    selected_route_id = request.session.get('selected_route')
    
    if not selected_route_id:
        messages.error(request, 'No route selected. Please select a route first.')
        return redirect('select_route')

    try:
        selected_route = Route.objects.get(pk=selected_route_id)
    except Route.DoesNotExist:
        messages.error(request, 'Selected route does not exist.')
        return redirect('select_route')

    if request.method == 'POST':
        form = TicketForm(request.POST, route=selected_route)  # Pass the selected route to the form
        if form.is_valid():
            # Save ticket with selected route
            ticket = form.save(commit=False)
            ticket.route = selected_route  # Set the route from session
            ticket.save()
            messages.success(request, 'Ticket successfully created!')
            return redirect('all_tickets')  # Redirect to all tickets or another page
    else:
        # Initialize form with selected route
        form = TicketForm(route=selected_route)  # Pass the selected route here as well

    return render(request, 'cut_ticket.html', {'form': form, 'selected_route': selected_route})


def all_tickets(request):
    tickets = Ticket.objects.all()
    return render(request, 'all_tickets.html', {'tickets': tickets})
    
