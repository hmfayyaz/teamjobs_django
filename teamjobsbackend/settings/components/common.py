"""
Django settings for teamjobsbackend project.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their config, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
from typing import Any, Tuple

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/
NOT_SECRET = "this is a bad secret key"  # nosec
SECRET_KEY = config("DJANGO_SECRET_KEY", default=NOT_SECRET)
GOOGLE_API_KEY = config("GOOGLE_API_KEY", default="")
PHONENUMBER_DEFAULT_REGION = "AU"
PHONENUMBER_DEFAULT_FORMAT = "INTERNATIONAL"

# Application definition:
FIXTURE_DIRS = [BASE_DIR / "teamjobsbackend" / "fixtures"]
SITE_ID = 1
LOCAL_APPS = (
    "users",
    "api",
)
THIRD_PARTY_APPS = (
    "whitenoise.runserver_nostatic",
    "address",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "anymail",
    "corsheaders",
    "django_quill",
    "django_jsonform",
    "dj_rest_auth",
    "dj_rest_auth.registration",
    # Health checks:
    # You may want to enable other checks as well,
    # see: https://github.com/KristianOellegaard/django-health-check
    "health_check",
    "health_check.db",
    "health_check.storage",
    # "knox",
    "localflavor",
    "phonenumber_field",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_serializer_extensions",
    "timezone_field",
    "import_export",
)

DJANGO_CORE_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # django-admin:
    "django.contrib.admin",
    "django.contrib.admindocs",
)
INSTALLED_APPS: Tuple[str, ...] = LOCAL_APPS + THIRD_PARTY_APPS + DJANGO_CORE_APPS

MIDDLEWARE: list[str] = [
    # Logging:
    "teamjobsbackend.settings.components.logging.LoggingContextVarsMiddleware",
    # Django:
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "users.middleware.TimezoneMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Django HTTP Referrer Policy:
]

ROOT_URLCONF = "teamjobsbackend.urls"

WSGI_APPLICATION = "teamjobsbackend.wsgi.application"

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-au"

USE_I18N = True
LOCALE_PATHS = [BASE_DIR / "locale"]

USE_TZ = True
TIME_ZONE = "UTC"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/


# Templates
# https://docs.djangoproject.com/en/3.2/ref/templates/api

TemplateEngineOptions = dict[Any, Any]
TemplatePaths = list[str]
TemplateConfig = dict[str, Any]
TEMPLATES: list[TemplateConfig] = [
    {
        "APP_DIRS": True,
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            # Contains plain text templates, like `robots.txt`:
            BASE_DIR.joinpath("teamjobsbackend", "templates"),
        ],
        "OPTIONS": {
            "context_processors": [
                # Default template context processors:
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",
            ],
        },
    }
]

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

ALLOWED_HOSTS = [
    config("DOMAIN_NAME", "api.teamjobs.com.au"),
    "localhost",
    "0.0.0.0",  # noqa: S104
    "127.0.0.1",
    "[::1]",
]

API_FACTORY_RESOURCE_PATH = BASE_DIR / "api" / "resources"
API_FACTORY_PATHS = {
    "areas": API_FACTORY_RESOURCE_PATH / "areas_goldcoast_sunshine_coast.csv",
    "addresses": API_FACTORY_RESOURCE_PATH / "gnaf_public_qld_addresses.csv",
    "categories": API_FACTORY_RESOURCE_PATH / "categories.csv",
    "certificates": API_FACTORY_RESOURCE_PATH / "certificates.csv",
}

DOMAIN_NAME = config("DOMAIN_NAME", default="api.teamjobs.com.au")

EMAIL_TIMEOUT = 5
DEFAULT_FROM_EMAIL = "noreply@teamjobs.com.au"
SERVER_EMAIL = "backend@teamjobs.com.au"
EMAIL_BACKEND = "anymail.backends.sendgrid.EmailBackend"
ANYMAIL = {
    "SENDGRID_API_KEY": config("SENDGRID_API_KEY", default=""),
}

MAIN_SITE_URL = config("MAIN_SITE_URL", "https://staging.teamjobs.com.au/")
MAIN_SITE_NAME = config("MAIN_SITE_NAME", "Team Jobs")
