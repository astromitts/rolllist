web: rm db-db-prod.sqlite3; python manage.py migrate --settings=project.settings_production; gunicorn project.wsgi --log-file -
