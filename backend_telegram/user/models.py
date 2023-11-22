from django.db import models


class User(models.Model):
    id = models.PositiveBigIntegerField(
        primary_key=True,
        unique=True,
        verbose_name='ID пользователя в Телеграмме'
    )
    username = models.CharField(max_length=100, blank=True, null=True)
    signed = models.BooleanField(default=False, verbose_name='Наличие подписки')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.id}'
