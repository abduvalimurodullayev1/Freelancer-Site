from django.urls import path
from apps.freelance import consumer

websocket_urlpatterns = [
    path('ws/group/<int:group_id>/', consumer.PrivateChatConsumer.as_asgi()),
]