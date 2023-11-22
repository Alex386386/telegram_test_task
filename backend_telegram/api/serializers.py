from rest_framework import serializers

from message.models import Message, BotText, CurrencyRate
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'signed']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['user', 'date', 'text']


class BotTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotText
        fields = ['title', 'text']


class CurrencyRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyRate
        fields = ['code', 'rate']
