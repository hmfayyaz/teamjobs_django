"""
Django settings for teamjobsbackend project.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their config, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

# Security
# https://docs.djangoproject.com/en/3.2/topics/security/

SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
CSRF_TRUSTED_ORIGINS = [f"https://{config('DOMAIN_NAME', 'api.teamjobs.com.au')}"]
X_FRAME_OPTIONS = "DENY"

# https://github.com/DmytroLitvinov/django-http-referrer-policy
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy
REFERRER_POLICY = "same-origin"

# CORS
CORS_ALLOWED_ORIGINS = [
    "https://staging.teamjobs.com.au",
    "https://www.teamjobs.com.au",
    f"https://{config('DOMAIN_NAME', 'api.teamjobs.com.au')}",
    "https://team-jobs.vercel.app",
    "http://localhost:8080",
    "http://localhost:3000",
    "https://teamjobs.com.au",
]

CORS_URLS_REGEX = r"^/api/.*$"
CORS_ALLOW_CREDENTIALS = True
