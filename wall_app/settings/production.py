from .settings import *

ALLOWED_HOSTS = ['*']

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ['PSQL_HOST'],
        'NAME': os.environ['PSQL_DB_NAME'],
        'USER': os.environ['PSQL_DB_USER'],
        'PASSWORD': os.environ['PSQL_DB_PASSWORD'],
    }
}


