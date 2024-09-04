from . import views
from django.urls import path

urlpatterns = [
    path("manager_signup/", views.manager_signup, name="manager_signup"),
    path("manager_login/", views.manager_login, name="manager_login"),
    path("manager_dashboard/", views.manager_dashboard, name="manager_dashboard"),
    path("manage_route/", views.manage_route, name="manage_route"),
    path("manage_stage/", views.manage_stage, name="manage_stage"),
    path("add_car/", views.add_car, name="add_car"),
    path("view_all/", views.view_all, name="view_all"),
    path("delete_car/<int:id>/", views.delete_car, name="delete_car"),
    path("delete_route/<int:route_id>/", views.delete_route, name="delete_route"),
    path("delete_stage/<int:id>/", views.delete_stage, name="delete_stage"),
    path("update_car/<int:id>/", views.update_car, name="update_car"),
    path("update_route/<int:route_id>/", views.update_route, name="update_route"),
]
