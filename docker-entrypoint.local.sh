#!/bin/sh
python3 manage.py collectstatic --noinput
#python manage.py makemigrations --merge --noinput
python3 manage.py migrate --noinput
pip install -r requirements.txt
python manage.py runserver 8000
