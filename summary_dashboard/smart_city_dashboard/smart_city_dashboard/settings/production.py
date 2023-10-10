import os
from .base import *

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
        'NAME': os.getenv('POSTGRES_DB', 'smartcitydb'),
        'USER': os.getenv('POSTGRES_USER', 'smartcityadmin'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'smart_city@admin_password'),
    }
}

HUEY = {
    'huey_class': 'huey.RedisHuey',  # Huey implementation to use.
    'name':"redis_huey",  # Use db name for huey.
    'results': True,  # Store return values of tasks.
    'store_none': False,  # If a task returns None, do not save to results.
    'immediate': False,  # If DEBUG=True, run synchronously.
    'utc': True,  # Use UTC for all times internally.
    'blocking': True,  # Perform blocking pop rather than poll Redis.
    'connection': {
        'host': os.getenv('REDIS_HOST', 'localhost'),
        'port': os.getenv('REDIS_PORT', 6379),
        'db': 0,
        'connection_pool': None,  # Definitely you should use pooling!
        # ... tons of other options, see redis-py for details.

        # huey-specific connection parameters.
        'read_timeout': 1,  # If not polling (blocking pop), use timeout.
        'url': None,  # Allow Redis config via a DSN.
    },
    'consumer': {
        'workers': 2,
        'worker_type': 'thread',
        'initial_delay': 0.3,  # Smallest polling interval, same as -d.
        'backoff': 1.15,  # Exponential backoff using this rate, -b.
        'max_delay': 10.0,  # Max possible polling interval, -m.
        'scheduler_interval': 60,  # Check schedule every second, -s.
        'periodic': True,  # Enable crontab feature.
        'check_worker_health': True,  # Enable worker health checks.
        'health_check_interval': 60,  # Check worker health every second.
    },
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = os.getenv('STATIC_URL', '/dashboard/static/')
MEDIA_URL = os.getenv('MEDIA_URL', '/media/')


STATIC_ROOT = os.path.join(BASE_DIR.parent,'storage/static')
MEDIA_ROOT = os.path.join(BASE_DIR.parent,'storage/media')


CSRF_TRUSTED_ORIGINS = [*os.getenv('CSRF_TRUSTED_ORIGINS','*').replace(' ','').split(',')]
USE_X_FORWARDED_HOST = True

