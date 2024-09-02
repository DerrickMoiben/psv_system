from . import views
from django.urls import path

urlpatterns = [
    path("manager_signup/", views.manager_signup, name="manager_signup"),
    path("manager_login/", views.manager_login, name="manager_login"),
    path("manager_dashboard/", views.manager_dashboard, name="manager_dashboard"),
]
