from urllib import parse

from allauth.account import forms as allauth_forms
from allauth.account.adapter import get_adapter
from allauth.account.utils import user_pk_to_url_str
from django.conf import settings
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import TeamUser


class TeamUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = TeamUser
        fields = ("first_name", "last_name", "email", "phone", "timezone")


class TeamUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = TeamUser
        fields = ("first_name", "last_name", "email", "phone", "timezone")


class ResetPasswordForm(allauth_forms.ResetPasswordForm):
    def _send_password_reset_mail(self, request, email, users, **kwargs):
        token_generator = kwargs.get(
            "token_generator", allauth_forms.default_token_generator
        )

        for user in users:
            temp_key = token_generator.make_token(user)
            user_pk = user_pk_to_url_str(user)
            url = parse.urljoin(
                settings.MAIN_SITE_URL, f"/accounts/password/reset/{user_pk}/{temp_key}"
            )
            context = {
                "current_site": {
                    "domain": parse.urlparse(settings.MAIN_SITE_URL).netloc,
                    "name": settings.MAIN_SITE_NAME,
                },
                "user": user,
                "password_reset_url": url,
                "request": request,
            }
            get_adapter(request).send_mail(
                "account/email/password_reset_key", email, context
            )
