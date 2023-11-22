FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements_telegram.txt

CMD python telegram_bot.py