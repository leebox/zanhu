# -*- coding:utf8 -*-
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import zanhu.chat.routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            zanhu.chat.routing.websocket_urlpatterns
        )
    ),
})