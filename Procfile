web: rm db-production.sqlite;python manage.py migrate --settings=project.settings_production; gunicorn project.wsgi --log-file -
