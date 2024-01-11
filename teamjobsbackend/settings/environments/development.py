"""
This file contains all the settings that defines the development server.

SECURITY WARNING: don't run with debug turned on in production!
"""

import logging
import mimetypes
import socket

# Setting the development status:

DEBUG = True

mimetypes.add_type("application/javascript", ".js", True)

DEBUG_TOOLBAR_CONFIG = {
    "INTERCEPT_REDIRECTS": False,
}

# Installed apps for development only:
# INSTALLED_APPS from components/common
INSTALLED_APPS += (
    # Better debug:
    "debug_toolbar",
    # "nplusone.ext.django",
    # django-extra-checks:
    "extra_checks",
)

# Django debug toolbar:
# https://django-debug-toolbar.readthedocs.io
# MIDDLEWARE from components/common
MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    # https://github.com/bradmontgomery/django-querycount
    # Prints how many queries were executed, useful for the APIs.
    # "querycount.middleware.QueryCountMiddleware",
]

# https://django-debug-toolbar.readthedocs.io/en/stable/installation.html#configure-internal-ips
try:  # This might fail on some OS
    INTERNAL_IPS = [
        f"{ip[:ip.rfind('.')]}.1"
        for ip in socket.gethostbyname_ex(socket.gethostname())[2]
    ]
except socket.error:  # pragma: no cover
    INTERNAL_IPS = []
INTERNAL_IPS += ["127.0.0.1", "10.0.2.2"]


def _custom_show_toolbar(request) -> bool:
    """Only show the debug toolbar to users with the superuser flag."""
    return DEBUG and request.user.is_superuser


DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": ("teamjobsbackend.settings._custom_show_toolbar"),
}

# This will make debug toolbar to work with django-csp,
# since `ddt` loads some scripts from `ajax.googleapis.com`:
# CSP_SCRIPT_SRC = ("'self'", 'ajax.googleapis.com')
# CSP_IMG_SRC = ("'self'", 'data:')
# CSP_CONNECT_SRC = ("'self'",)

# nplusone
# https://github.com/jmcarp/nplusone

# Should be the first in line:
MIDDLEWARE = [  # noqa: WPS440
    # "nplusone.ext.django.NPlusOneMiddleware",
] + MIDDLEWARE

# Logging N+1 requests:
NPLUSONE_RAISE = True  # comment out if you want to allow N+1 requests
NPLUSONE_LOGGER = logging.getLogger("django")
NPLUSONE_LOG_LEVEL = logging.WARN
NPLUSONE_WHITELIST = [
    {"model": "admin.*"},
]

EXTRA_CHECKS = {
    "checks": [
        # Each model must be registered in admin:
        "model-admin",
        # FileField/ImageField must have non-empty `upload_to` argument:
        "field-file-upload-to",
        # Text fields shouldn't use `null=True`:
        "field-text-null",
        # Don't pass `null=False` to model fields (this is django default)
        "field-null",
        # ForeignKey fields must specify db_index explicitly if used in
        # other indexes:
        {"id": "field-foreign-key-db-index", "when": "indexes"},
        # If field nullable `(null=True)`,
        # then default=None argument is redundant and should be removed:
        "field-default-null",
    ],
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "teamjobs.db",
    },
}

WHITENOISE_USE_FINDERS = True
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
MAIN_SITE_URL = config("MAIN_SITE_URL", "http://localhost:3000/")
