import os

import requests
from celery import shared_task
from .models import CurrencyRate

token = os.getenv('ACCESS_TOKEN')


@shared_task
def fetch_and_update_currency_rates():
    url = f'http://data.fixer.io/api/latest?access_key={token}'
    response = requests.get(url)
    data = response.json()
    if data.get('success'):
        rates = data.get('rates')
        for code, rate in rates.items():
            CurrencyRate.objects.update_or_create(code=code, defaults={'rate': rate})
