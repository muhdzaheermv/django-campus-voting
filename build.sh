#!/usr/bin/env bash

# Install requirements ONLY if pip freeze shows no Django
if ! pip freeze | grep -q Django; then
  echo "Installing dependencies..."
  pip install -r requirements.txt
fi

python manage.py collectstatic --noinput
python manage.py migrate

if [[ -n "${CREATE_SUPERUSER}" ]]; then
  echo "Creating Django superuser..."
  echo "
from django.contrib.auth import get_user_model
User = get_user_model()
username = '${DJANGO_SUPERUSER_USERNAME}'
email = '${DJANGO_SUPERUSER_EMAIL}'
password = '${DJANGO_SUPERUSER_PASSWORD}'
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print('Superuser created.')
else:
    print('Superuser already exists.')
" | python manage.py shell
fi
