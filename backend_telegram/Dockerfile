FROM python:3.11-alpine

WORKDIR /app


RUN pip install --upgrade pip

COPY . .

RUN pip3 install --upgrade pip \
    && pip3 install -r requirements.txt --no-cache-dir \
    && mkdir -p /app/logs \
    && chmod +x entrypoint.sh \
    && mkdir -p /app/tmp

ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["gunicorn", "backend_telegram.wsgi:application", "--bind", "0:8000" ]
