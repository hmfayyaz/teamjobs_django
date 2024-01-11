"""
This is a django-split-settings main file.

For more information read this:
https://github.com/sobolevn/django-split-settings
https://sobolevn.me/2017/04/managing-djangos-settings

To change settings file:
`DJANGO_ENV=production python manage.py runserver`
"""
import os
from pathlib import Path
from typing import TYPE_CHECKING

from decouple import AutoConfig
from dotenv import load_dotenv
from split_settings.tools import include, optional

if TYPE_CHECKING:
    import django_stubs_ext

    # Monkeypatching Django, so stubs will work for all generics,
    # see: https://github.com/typeddjango/django-stubs
    django_stubs_ext.monkeypatch()

_NOTASECRET = "--set-a-real-secret-please--"
# `pathlib` is better than writing: dirname(dirname(dirname(__file__)))
BASE_DIR = Path(__file__).parent.parent.parent
# Loading `.env` files
env_map = {
    "development": ".env",
    "production": ".env.production",
    "staging": ".env.staging",
    "tests": ".env.ci",
}
_ENV = os.environ.get("DJANGO_ENV", "development")
load_dotenv(BASE_DIR / env_map.get(_ENV))
# See docs: https://gitlab.com/mkleehammer/autoconfig
config = AutoConfig()

_base_settings = (
    "components/common.py",
    "components/storage_and_files.py",
    "components/logging.py",
    "components/rest.py",
    "components/user_auth.py",
    "components/security_headers.py",
)

# Include settings:
include(*_base_settings, scope=globals())
# print(globals())
include(f"environments/{_ENV}.py", scope=globals())
include(optional("environments/local.py"), scope=globals())
