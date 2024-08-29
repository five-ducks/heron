#!/bin/env sh
# python manage.py makemigrations chat games profiles notice

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --no-input --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL || true
python manage.py shell -c "from users.models import User; user=User.objects.get(username='$DJANGO_SUPERUSER_USERNAME'); user.set_password('$DJANGO_SUPERUSER_PASSWORD'); user.save()"

exec python manage.py runserver 0.0.0.0:8000
