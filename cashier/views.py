from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from .forms import CashierSignupForm, TicketForm, RouteSelectionForm, CarselectionForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseForbidden
from .models import Route, Ticket
import json
from django.http import JsonResponse

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
            return redirect('select_car')
        except Route.DoesNotExist:
            messages.error(request, 'Selected route does not exist')
            return redirect('select_route')
    else:
        form = RouteSelectionForm()
    return render(request, 'select_route.html', {'form': form})


from manager.models import Car
from django.shortcuts import get_object_or_404

def select_car(request):
    selected_route_id = request.session.get('selected_route')  # Get the sected_route_id
    
    if not selected_route_id:
        messages.error(request, 'No route selected. Please select a route first.')
        return redirect('select_route')
    
    selected_route = get_object_or_404(Route, pk=selected_route_id)
    
    if request.method == 'POST':
        form = CarselectionForm(request.POST, route=selected_route)
        if form.is_valid():
            car_id = form.cleaned_data['car'].id
            request.session['selected_car'] = car_id
            return redirect('cut_ticket')
    else:
        form = CarselectionForm(route=selected_route)
    return render(request, 'select_car.html', {'form': form, 'selected_route': selected_route}) 
    
    
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import TicketForm
from .models import Route, StagePrice

def cut_ticket(request):
    selected_route_id = request.session.get('selected_route')
    
    if not selected_route_id:
        messages.error(request, 'No route selected. Please select a route first.')
        return redirect('select_route')

    try:
        selected_route = Route.objects.get(pk=selected_route_id)
        stage_prices = StagePrice.objects.filter(route=selected_route) \
                      .select_related('stage') \
                      .only('stage_id', 'price')
    except Route.DoesNotExist:
        messages.error(request, 'Selected route does not exist.')
        return redirect('select_route')

    # Create a dictionary mapping stage IDs to prices
    price_mapping = {sp.stage_id: sp.price for sp in stage_prices}

    if request.method == 'POST':
        form = TicketForm(request.POST or None, route=selected_route)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.route = selected_route
            alighting_stage = form.cleaned_data['alighting_stage']
            
            # Use pre-fetched prices
            if (ticket_price := price_mapping.get(alighting_stage.id)) is not None:
                ticket.price = ticket_price
                ticket.save()
                messages.success(request, 'Ticket successfully created!')
                request.session.modified = True  # Security fix
                return redirect('all_tickets')
            
            messages.error(request, 'Price for selected stage not found')
            return render(request, 'cut_ticket.html', {
                'form': form,
                'selected_route': selected_route,
                'stage_prices': price_mapping
            })

    else:
        form = TicketForm(route=selected_route)

    return render(request, 'cut_ticket.html', {
        'form': form,
        'selected_route': selected_route,
        'stage_prices': price_mapping
    })

from django.http import JsonResponse
from manager.models import StagePrice

def get_stage_price(request, stage_id):
    try:
        # Assuming you have a way to get the route from session or request
        route_id = request.session.get('selected_route')
        if not route_id:
            return JsonResponse({'error': 'No route selected'}, status=400)

        # Get the price for the selected stage and route
        stage_price = StagePrice.objects.get(stage_id=stage_id, route_id=route_id)
        return JsonResponse({'price': str(stage_price.price)})
    except StagePrice.DoesNotExist:
        return JsonResponse({'price': None})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def all_tickets(request):
    tickets = Ticket.objects.all()
    return render(request, 'all_tickets.html', {'tickets': tickets})
    
from django.http import JsonResponse, HttpResponseBadRequest
import json

def mpesa_callback(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print("MPESA Callback Data:", data)
            return JsonResponse({"status": "success"}, status=200)
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON")
    else:
        return HttpResponseBadRequest("Invalid request method")
