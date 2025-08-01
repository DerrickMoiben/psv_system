# This file contains the views for the manager app  
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from .forms import ManagerLoginForm, ManagerSingupForm, RouteForm, StageForm, CarForm, StagePriceFormSet
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .models import Route, Stage, Car, StagePrice
from django.http import HttpResponseForbidden
from cashier.models import Ticket
from cashier.forms import TicketForm


# def custom_login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
            
#             # Check the user's role and redirect accordingly
#             if user.role == 'manager':
#                 return redirect('manager_dashboard')
#             elif user.role == 'cashier':
#                 return redirect('cashier_dashboard')
#             else:
#                 return render(request, 'login.html', {'errors': 'Unknown user role'})

#         else:
#             return render(request, 'login.html', {'errors': 'Invalid credentials'})

#     return render(request, 'login.html')


@csrf_protect
def manager_signup(request):
    if request.method == 'POST':
        form = ManagerSingupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'manager'  # Explicitly set the role to manager
            user.save()
            messages.success(request, 'Account created successfully')
            return redirect('manager_login')
        else:
            messages.error(request, 'An error occurred during registration')
            print(form.errors)
            
    else:
        form = ManagerSingupForm()
    return render(request, 'signup.html', {'form': form})


@csrf_protect
def manager_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None and user.role == 'manager':
            login(request, user)
            return redirect('manager_dashboard')  # Redirect to manager dashboard
        else:
            return render(request, 'login.html', {'errors': 'Invalid credentials or not a manager'})
    return render(request, 'login.html')

@login_required 

def manager_dashboard(request):
    total_cars = Car.objects.count()
    total_routes = Route.objects.count()
    total_stages = Stage.objects.count()
    context = {
        'total_cars': total_cars,
        'total_routes': total_routes,
        'total_stages': total_stages,
    }
    return render(request, 'dashboard.html', context)

def manager_logout(request):
    return render(request, 'logout.html')

def manager_profile(request):
    return render(request, 'profile.html')


def manage_route(request):
    if request.method == 'POST':
        form = RouteForm(request.POST)
        if form.is_valid():
            route = form.save()
            
            # Get selected stages
            selected_stages = form.cleaned_data['stage']
            stage_prices = []
            for stage in selected_stages:
                price = request.POST.get(f'price_{stage.id}')  # Get price for each stage
                if price:
                    stage_prices.append(StagePrice(route=route, stage=stage, price=price))
            
            # Save all stage prices
            StagePrice.objects.bulk_create(stage_prices)
            messages.success(request, 'Route and prices added successfully')
            return redirect('view_all')
        else:
            messages.error(request, 'An error occurred during route registration')
            print(form.errors)
    else:
        form = RouteForm()
    
    return render(request, 'route.html', {'form': form})


def manage_stage(request):
    if request.method == 'POST':
        form = StageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Stage has been added sucessfully')
            return redirect('view_all')
        else:
            messages.error(request, 'An error occured while tyring to addd a new stage')
            print(form.errors)
    else:
        form = StageForm()
    return render(request, 'stage.html', {'form': form})

def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Car was added sucessfuyy to the sytem')
            return redirect('view_all')
        else:
            messages.error(request, 'An error occured while tyring to addd a new car')
            print(form.errors)
    else:
        form = CarForm()
        return render(request, 'car.html', {'form': form})
    
def view_all(request):
    cars = Car.objects.all()
    routes = Route.objects.prefetch_related('stage', 'stage_prices').all()
    stages = Stage.objects.all()
    return render(request, 'view_all.html', {'cars': cars, 'routes': routes, 'stages': stages})


def delete_car(request, id):
    try:
        cars = Car.objects.get(id=id)
        cars.delete()
        messages.success(request, 'You have successuly deleted the car')
    except Car.DoesNotExist:
        messages.error(request, 'The car does not exist')
    return redirect(view_all)


def delete_route(request, route_id):
    try:
        routes = Route.objects.get(route_id=route_id)
        routes.delete()
        messages.success(request, 'You have successuly deleted the route')
    except Route.DoesNotExist:
        messages.error(request, 'The route does not exist')
    return redirect(view_all)

def delete_stage(request, id):
    try:
        stages = Stage.objects.get(id=id)
        stages.delete()
        messages.success(request, 'You have successuly deleted the stage')
    except Stage.DoesNotExist:
        messages.error(request, 'The stage does not exist')
    return redirect(view_all)

def update_car(request, id):
    car = get_object_or_404(Car, id=id)
    if request.method == 'POST':
        form = CarForm(request.POST, instance=car)
        if form.is_valid():
            form.save()
            messages.success(request, 'Car updated successfully')
            return redirect('view_all')
        else:
            messages.error(request, 'An error occured while tyring to update the car')
            # print(form.errors)
    else:
        form = CarForm(instance=car)
    return render(request, 'update_car.html', {'form': form, 'car': car})


def update_route(request, route_id):
    route = get_object_or_404(Route, route_id=route_id)
    stage_prices = StagePrice.objects.filter(route=route)
    
    if request.method == 'POST':
        form = RouteForm(request.POST, instance=route)
        stage_price_formset = StagePriceFormSet(request.POST, queryset=stage_prices)
        
        if form.is_valid() and stage_price_formset.is_valid():
            route = form.save()
            stage_prices = stage_price_formset.save(commit=False)
            
            for stage_price in stage_prices:
                stage_price.route = route
                stage_price.save()
            
            messages.success(request, 'You have successfully updated the route and prices')
            return redirect('view_all')
        else:
            messages.error(request, 'There was an error while trying to update the route and prices')
            print(form.errors)
            print(stage_price_formset.errors)
    else:
        form = RouteForm(instance=route)
        stage_price_formset = StagePriceFormSet(queryset=stage_prices)
    
    return render(request, 'update_route.html', {'form': form, 'stage_price_formset': stage_price_formset, 'object': route})

def update_stage(request, id):
    stage = get_object_or_404(Stage, id=id)
    if request.method == 'POST':
        form = StageForm(request.POST, instance=stage)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully updated the stage')
            return redirect(view_all)
        else:
            messages.error(request, 'An error occured while trying to update the stage')
            print(form.errors)
            print(form.data)
    else:
        form = StageForm(instance=stage)
    return render(request, 'update_stage.html', {'form': form, 'object': stage})   

from django.http import JsonResponse
from .models import Stage

def load_stages(request):
    city_id = request.GET.get('city_id')
    stages = Stage.objects.filter(city_id=city_id).order_by('stage_name')
    return render(request, 'stages_dropdown_list_options.html', {'stages': stages})



import requests
import base64
import json
import os
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

MPESA_CONSUMER_KEY = os.getenv('MPESA_CONSUMER_KEY')
MPESA_CONSUMER_SECRET = os.getenv('MPESA_CONSUMER_SECRET')
MPESA_SHORTCODE = os.getenv('MPESA_SHORTCODE')
MPESA_PASSKEY = os.getenv('MPESA_PASSKEY')
MPESA_CALLBACK_URL = os.getenv('MPESA_CALLBACK_URL')



import requests
import json
import base64
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render

# Replace these with your actual credentials
MPESA_CONSUMER_KEY = "YOUR_CONSUMER_KEY"
MPESA_CONSUMER_SECRET = "YOUR_CONSUMER_SECRET"
MPESA_SHORTCODE = "YOUR_SHORTCODE"
MPESA_PASSKEY = "YOUR_PASSKEY"
MPESA_CALLBACK_URL = "YOUR_CALLBACK_URL"

# Change this to `sandbox.safaricom.co.ke` if testing
MPESA_ENVIRONMENT = "api.safaricom.co.ke"

def get_mpesa_access_token():
    url = "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    
    # Encode Consumer Key and Secret
    credentials = f"{MPESA_CONSUMER_KEY}:{MPESA_CONSUMER_SECRET}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded_credentials}",
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        access_token = response.json().get("access_token", None)
        if access_token:
            return access_token
        else:
            raise Exception("Failed to retrieve access token: No token received.")
    except requests.exceptions.HTTPError as http_err:
        raise Exception(f"HTTP error occurred: {http_err}")
    except Exception as err:
        raise Exception(f"Other error occurred: {err}")


def stk_push_payment(request):
    if request.method == "POST":
        phone_number = request.POST.get("phone_number")  # Get phone number from form
        amount = request.POST.get("amount")  # Get amount from form

        if not phone_number or not amount:
            return JsonResponse({"error": "Phone number and amount are required"}, status=400)

        # Validate and format the phone number
        if phone_number.startswith("0"):
            phone_number = "254" + phone_number[1:]
        elif phone_number.startswith("+"):
            phone_number = phone_number[1:]

        if not phone_number.startswith("254"):
            return JsonResponse({"error": "Invalid phone number format"}, status=400)

        try:
            access_token = get_mpesa_access_token()
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

        print("Access Token:", access_token)

        # Generate timestamp and password
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        data_to_encode = MPESA_SHORTCODE + MPESA_PASSKEY + timestamp
        password = base64.b64encode(data_to_encode.encode()).decode('utf-8')

        stk_url = f"https://{MPESA_ENVIRONMENT}/mpesa/stkpush/v1/processrequest"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "BusinessShortCode": MPESA_SHORTCODE,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerBuyGoodsOnline",  # Use the correct type
            "Amount": int(amount),
            "PartyA": phone_number,
            "PartyB": MPESA_SHORTCODE,
            "PhoneNumber": phone_number,
            "CallBackURL": MPESA_CALLBACK_URL,
            "AccountReference": "5501810",
            "TransactionDesc": "Payment for Order"
        }

        response = requests.post(stk_url, json=payload, headers=headers)

        # Print debug information
        print("STK Push Response Status:", response.status_code)
        print("STK Push Response Content:", response.text)

        try:
            return JsonResponse(response.json())
        except json.JSONDecodeError:
            return JsonResponse({"error": "Failed to process STK Push request"}, status=500)

    return render(request, "stk_push.html")




from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def mpesa_callback(request):
    if request.method == "POST":
        try:
            mpesa_response = json.loads(request.body)
            print("M-Pesa Callback Response:", mpesa_response)  # Debugging

            # Handle response logic (e.g., save transaction details to the database)
            
            return JsonResponse({"message": "Callback received successfully"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)
