from os import getenv, path
from dotenv import load_dotenv
from .base import *  # noqa
from .base import BASE_DIR

local_env_file = path.join(BASE_DIR, '.envs', ".env.local")

if path.isfile(local_env_file):
    load_dotenv(local_env_file)




DEBUG = True

SITE_NAME = getenv('SITE_NAME')

SECRET_KEY = getenv(
    'SECRET_KEY', "django-insecure-8k_lm&mvhye&i-_e%l3m5r&w_7f8c%d3l^f@mpc*ra5f%q&898"
    )

ALLOWED_HOSTS = ["*"]

ADMIN_URL = getenv('DJANGO_ADMIN_URL')
EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
EMAIL_HOST = getenv('EMAIL_HOST')
EMAIL_PORT = getenv('EMAIL_PORT')
DEFAULT_FORM_EMAIL = getenv('DEFAULT_FORM_EMAIL')
DOMAIN = getenv('DOMAIN')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters':{
        'verbose': {
            'verbose': {
                'format': '%(levelname)s %(name)-12s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            }
        },

    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root':{
        'lavel': 'INFO',
        "handlers": ['console'],
    }
}