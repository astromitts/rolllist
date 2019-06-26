from project.settings import *  # noqa
import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db-dev.sqlite3'),  # noqa
    }
}


ALLOWED_HOSTS = ['localhost', '127.0.0.1']
