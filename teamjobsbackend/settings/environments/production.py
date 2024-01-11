"""
This file contains all the settings used in production.

This file is required and if development.py is present these
values are overridden.
"""

from django.core.exceptions import ImproperlyConfigured

if SECRET_KEY == NOT_SECRET:
    raise ImproperlyConfigured("SECRET_KEY has not been set on a production server!")

# Production flags:
# https://docs.djangoproject.com/en/3.2/howto/deployment/

DEBUG = False

ALLOWED_HOSTS = [
    # TODO: check production hosts
    config("DOMAIN_NAME", "api.teamjobs.com.au"),
    # We need this value for `healthcheck` to work:
    "localhost",
]

# Security
# https://docs.djangoproject.com/en/3.2/topics/security/

SECURE_HSTS_SECONDS = 60  # the same as Caddy has
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
SECURE_REDIRECT_EXEMPT = [
    # This is required for healthcheck to work:
    "^health/",
]

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS += ["https://*.teamjobs.com.au"]
CSRF_COOKIE_DOMAIN = ".teamjobs.com.au"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DJANGO_POSTGRES_DB", default="teamjobs"),
        "USER": config("DJANGO_POSTGRES_USER", default="teamjobs"),
        "PASSWORD": config("DJANGO_POSTGRES_PASSWORD", default=""),
        "HOST": config("DJANGO_DATABASE_HOST", default="localhost"),
        "PORT": config("DJANGO_DATABASE_PORT", cast=int, default=5432),
        "CONN_MAX_AGE": config("CONN_MAX_AGE", cast=int, default=60),
        "OPTIONS": {
            "connect_timeout": 10,
            "options": "-c statement_timeout=15000ms",
        },
    }
}
