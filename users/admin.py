from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import TeamUserChangeForm, TeamUserCreationForm
from .models import TeamUser

# Register your models here.


class TeamUserAdmin(UserAdmin):
    add_form = TeamUserCreationForm
    form = TeamUserChangeForm
    model = TeamUser
    list_display = (
        "email",
        "first_name",
        "last_name",
        "last_login",
        "is_superuser",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "first_name",
        "last_name",
        "email",
        "last_login",
        "is_superuser",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("first_name", "last_name", "password")}),
        (_("Personal info"), {"fields": ("email", "phone", "timezone")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "phone",
                    "timezone",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    search_fields = ("name", "email")
    ordering = ("email",)


admin.site.register(TeamUser, TeamUserAdmin)
