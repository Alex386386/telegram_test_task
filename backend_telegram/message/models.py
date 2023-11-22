import uuid

from django.db import models

from user.models import User


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    class Meta:
        verbose_name = 'Сообщение пользователя'
        verbose_name_plural = 'Сообщения пользователей'

    def __str__(self):
        return f'{self.text}'


class BotText(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, unique=True)
    text = models.TextField()

    class Meta:
        verbose_name = 'Сообщение бота'
        verbose_name_plural = 'Сообщения бота'

    def __str__(self):
        return self.title


class CurrencyRate(models.Model):
    code = models.CharField(max_length=3, primary_key=True)
    rate = models.DecimalField(max_digits=20, decimal_places=6)

    class Meta:
        verbose_name = 'Курс валюты'
        verbose_name_plural = 'Курсы валют'

    def __str__(self):
        return f"{self.code}: {self.rate}"
