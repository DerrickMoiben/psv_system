from django.shortcuts import render

# Create your views here.\

def index(request):
    return render(request, 'index.html')


def cashier_dashboard(request):
    return render(request, 'cashier_dashboard.html')
