import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import transport_system.routing # import websocket_urlpatterns
from django.conf import settings
from django.conf.urls.static import static


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'transport_system.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            transport_system.routing.websocket_urlpatterns
        )
    ),
    "static": static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
    "media": static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
})
