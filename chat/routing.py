# from django.urls import path

# from .consumers import ChatConsumer
# websocket_urlpatterns = [
#     path('ws/chat/', ChatConsumer.as_asgi()),
# ]



from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/chat/<int:thread_id>/', consumers.ChatConsumer.as_asgi()),
]

