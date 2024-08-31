from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/transport_system/', consumers.MyConsumer.as_asgi()),
]
