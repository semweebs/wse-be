migrate: bash deployment.sh
release: python manage.py migrate
web: gunicorn wsebe.wsgi --log-file -
