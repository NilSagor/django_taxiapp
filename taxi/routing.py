from channels.routing import ProtocolTypeRouter, URLRouter 

from django.urls import path
from channels.auth import AuthMiddlewareStack
from trips.consumers import TaxiConsumer

application = ProtocolTypeRouter({
	'websocket': AuthMiddlewareStack(
		URLRouter([
			path('taxi/', TaxiConsumer),
			])
		)
	})