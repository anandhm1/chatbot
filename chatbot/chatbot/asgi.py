"""
ASGI config for chatbot project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatbot.settings')

# application = get_asgi_application()
# import os
# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# from chat.routing import websocket_urlpatterns
# from .middleware import JWTAuthMiddleware



# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatbot.settings')

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": JWTAuthMiddleware(
#         URLRouter(websocket_urlpatterns)
#     ),
# })
# import os

# from channels.routing import URLRouter, ProtocolTypeRouter
# from channels.security.websocket import AllowedHostsOriginValidator  # new
# from django.core.asgi import get_asgi_application
# from chat import routing  # new
# from .middleware import TokenAuthMiddleware  # new

# # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ChatAPI.settings')

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AllowedHostsOriginValidator(  # new
#         TokenAuthMiddleware(URLRouter(routing.websocket_urlpatterns)))
# })
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from chatbot.middleware import JWTAuthMiddleware
from chat.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatbot.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JWTAuthMiddleware(
        URLRouter(websocket_urlpatterns)
    ),
})

