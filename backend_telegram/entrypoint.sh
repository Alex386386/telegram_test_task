#!/bin/sh

FLAG_FILE="/app/tmp/entrypoint_has_run.flag"

if [ ! -f "$FLAG_FILE" ]; then
    echo "Ожидание подключения к базе данных..."
    while ! nc -z db 5432; do
      sleep 1
    done
    echo "База данных запущена"

    python manage.py makemigrations
    python manage.py migrate
    python manage.py load_all_data
    python manage.py collectstatic --no-input --clear
    echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('example', 'myemail@example.com', 'example')" | python manage.py shell

    touch "$FLAG_FILE"
else
    echo "Скрипт entrypoint.sh уже был выполнен, пропускаем..."
fi

exec "$@"