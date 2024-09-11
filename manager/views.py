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


# def manager_city(request):
#     if request.method == 'POST':
#         form = CityForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'City added successfully')
#             return redirect('view_all')
#         else:
#             messages.error(request, 'An error occurred during registration' )
#             print(form.errors)
#     else:
#         form = CityForm()
#     return render(request, 'city.html', {'form': form})




# pushing for the green part mnazss
#tu push ya jana sasa 