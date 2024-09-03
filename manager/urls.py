from . import views
from django.urls import path

urlpatterns = [
    path("manager_signup/", views.manager_signup, name="manager_signup"),
    path("manager_login/", views.manager_login, name="manager_login"),
    path("manager_dashboard/", views.manager_dashboard, name="manager_dashboard"),
    path("manage_route/", views.manager_route, name="manage_route"),
    path("manage_stage/", views.manager_stage, name="manage_stage"),
    path("add_car/", views.add_car, name="add_car"),
]
