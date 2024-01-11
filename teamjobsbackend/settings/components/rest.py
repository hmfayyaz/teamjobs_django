"""
Django settings for teamjobsbackend project.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their config, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import hashids

HASH_IDS = hashids.Hashids(config("HASHID_SALT", ""))
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        # "knox.auth.TokenAuthentication",
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
    ],
    "SERIALIZER_EXTENSIONS": {
        "USE_HASH_IDS": True,
        "HASH_IDS_SOURCE": "teamjobsbackend.settings.HASH_IDS",
    },
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 100,
}

REST_AUTH = {
    "USER_DETAILS_SERIALIZER": "users.serializers.UserSerializer",
    "PASSWORD_RESET_SERIALIZER": "users.serializers.PasswordResetSerializer",
    "SESSION_LOGIN": False,
}
