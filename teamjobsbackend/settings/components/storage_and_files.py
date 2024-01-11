import pathlib

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
    "cv": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        "OPTIONS": {
            "location": BASE_DIR / "uploads" / "application_cvs",
            "file_permissions_mode": 0o600,
            "directory_permissions_mode": 0o700,
        },
    },
}

STATIC_ROOT = BASE_DIR / "static"
STATIC_URL = "/static/"
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)
# Media files
# Media root dir is commonly changed in production
# (see development.py and production.py).
# https://docs.djangoproject.com/en/3.2/topics/files/

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR.joinpath("media")

# Django authentication system
# https://docs.djangoproject.com/en/3.2/topics/auth/
# DEPRECATED(kept for migrations)
CV_WRAPPED_STORAGE_CLASS: str = "django.core.files.storage.FileSystemStorage"
CV_STORAGE_ARGS: dict[str, pathlib.Path | str] = {
    "location": BASE_DIR / "uploads" / "application_cvs",
    "file_permissions_mode": "0600",
    "directory_permissions_mode": "0700",
}
