from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cashier_dashboard/', views.cashier_dashboard, name='cashier_dashboard'),
    path('cashier_signup/', views.cashier_signup, name='cashier_signup'),
]