#!/bin/env sh

python manage.py makemigrations
python manage.py migrate
python manage.py shell -c "
from django.contrib.auth import get_user_model; 
User = get_user_model(); 
if not User.objects.filter(username='$DJANGO_SUPERUSER_NAME').exists(): 
    user = User.objects.create_superuser(username='$DJANGO_SUPERUSER_NAME', email='$DJANGO_SUPERUSER_EMAIL', password='$DJANGO_SUPERUSER_PASSWORD'); 
"
python manage.py clearsessions

exec dumb-init python manage.py runserver 0.0.0.0:8000
