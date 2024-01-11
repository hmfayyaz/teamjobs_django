from allauth.account.adapter import get_adapter
from dj_rest_auth import serializers as rest_serializers
from rest_framework import serializers
from timezone_field.rest_framework import TimeZoneSerializerField

from .forms import ResetPasswordForm
from .models import TeamUser


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user object."""

    timezone = TimeZoneSerializerField()

    def create(self, instance, validated_data):
        password = validated_data.pop("password", None)
        instance = super().create(instance, validated_data)
        if password is not None:
            password = get_adapter().clean_password(password, instance)
            get_adapter().set_password(instance, password)
        return instance

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        instance = super().update(instance, validated_data)
        if password is not None:
            password = get_adapter().clean_password(password, instance)
            get_adapter().set_password(instance, password)
        return instance

    class Meta:
        model = TeamUser
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "phone",
            "password",
            "timezone",
            "date_joined",
            "last_login",
        )
        read_only_fields = ["email"]
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}


class PasswordResetSerializer(rest_serializers.PasswordResetSerializer):
    password_reset_form_class = ResetPasswordForm
