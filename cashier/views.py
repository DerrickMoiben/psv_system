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



# cashier/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Ticket
from manager.models import Route, Car, Stage, StagePrice
from .forms import TicketForm

def cut_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            # Calculate the price based on route and stages
            price_obj = StagePrice.objects.get(route=ticket.route, stage=ticket.alighting_stage)
            ticket.price = price_obj.price
            ticket.cashier = request.user
            ticket.save()
            return redirect('ticket_success', ticket_id=ticket.id)
    else:
        form = TicketForm()
    return render(request, 'cut_ticket.html', {'form': form})

# View to dynamically load cars based on selected route
def load_cars(request):
    route_id = request.GET.get('route')
    cars = Car.objects.filter(route_id=route_id)
    return JsonResponse(list(cars.values('id', 'car_plate')), safe=False)

# View to dynamically load available seats based on selected car
def load_seats(request):
    car_id = request.GET.get('car')
    car = get_object_or_404(Car, id=car_id)
    taken_seats = car.tickets.values_list('seat_number', flat=True)
    available_seats = [i for i in range(1, car.seating_capacity + 1) if i not in taken_seats]
    return JsonResponse({'available_seats': available_seats})

# Ticket success page after cutting the ticket
def ticket_success(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    return render(request, 'ticket_success.html', {'ticket': ticket})
