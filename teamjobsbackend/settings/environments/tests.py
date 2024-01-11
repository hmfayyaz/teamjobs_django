from html_sanitizer import sanitizer

DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    },
}

HTML_SANITIZERS = {
    "testapp_sanitizer": {
        "tags": ["p", "br", "b", "i", "em", "strong", "a"],
        "element_preprocessors": [
            sanitizer.bold_span_to_strong,
            sanitizer.italic_span_to_em,
            sanitizer.tag_replacer("b", "strong"),
            sanitizer.tag_replacer("i", "em"),
        ],
        "element_postprocessors": [],
        "is_mergeable": lambda e1, e2: True,
        "whitespace": {"br"},
        "empty": ["br"],
        "keep_typographic_whitespace": False,
        "separate": {},
    }
}

INSTALLED_APPS += ("tests.testapp",)
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

SESSION_ENGINE = "django.contrib.sessions.backends.file"
API_FACTORY_RESOURCE_PATH = (
    BASE_DIR / "tests" / "api" / "factories" / "utils" / "resources"
)
#  API_FACTORY_PATHS from components/common
API_FACTORY_PATHS["addresses"] = API_FACTORY_RESOURCE_PATH / "addresses.csv"
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
