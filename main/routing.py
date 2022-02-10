from django.urls import path
from .consumers import WSConsumer, TweetConsumer

ws_urlpatterns = [
    path('ws/graph/', WSConsumer.as_asgi()),
    path('ws/tweet/', TweetConsumer.as_asgi()),
]