from django.urls import path, include
from rest_framework import routers

from .views import MessageViewSet, BotTextReadOnlyViewSet, UserViewSet, CurrencyRateReadOnlyViewSet

v1_router = routers.DefaultRouter()
v1_router.register('users', UserViewSet, basename='user')
v1_router.register(r'users/(?P<user_id>\d+)/messages', MessageViewSet, basename='message')
v1_router.register('bot-texts', BotTextReadOnlyViewSet, basename='bot-text')
v1_router.register('сurrency-rate', CurrencyRateReadOnlyViewSet, basename='сurrency-rate')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
