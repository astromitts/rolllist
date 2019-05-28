from project.settings import *  # noqa
import os

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dfklhffratb240',
        'USER': 'angyjgxjtmqkhp',
        'PASSWORD': 'ad970542e95ff459bb39232ae072b4d7e6f112f04c9949ac3706f61236650ee7',
        'HOST': 'ec2-54-243-241-62.compute-1.amazonaws.com',
        'PORT':'5432'
    }
}
# DATABASE_URL: postgres://angyjgxjtmqkhp:ad970542e95ff459bb39232ae072b4d7e6f112f04c9949ac3706f61236650ee7@ec2-54-243-241-62.compute-1.amazonaws.com:5432/dfklhffratb240