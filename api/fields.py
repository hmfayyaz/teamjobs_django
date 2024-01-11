import logging
from typing import Any

from django.core.exceptions import ImproperlyConfigured
from django.db import models
from html_sanitizer.django import get_sanitizer

logger = logging.getLogger(__name__)


class CleanHTMLField(models.TextField):
    description = "HTML field that is cleaned with a sanitizer"

    def __init__(self, *args: Any, **kwargs: dict[str, Any]):
        self.sanitizer_name = kwargs.pop("sanitizer", "default")
        try:
            self.sanitizer = get_sanitizer(self.sanitizer_name)
        except ImproperlyConfigured as e:
            logger.error(
                "Unable to load sanitizer %s: %s falling back to default",
                self.sanitizer_name,
                e,
            )
            self.sanitizer = get_sanitizer("default")
        super().__init__(*args, **kwargs)

    def deconstruct(self) -> tuple[str, str, list[Any], dict[str, Any]]:
        name, path, args, kwargs = super().deconstruct()
        if self.sanitizer_name != "default":
            kwargs["sanitizer"] = self.sanitizer_name
        return name, path, args, kwargs

    @property
    def non_db_attrs(self):
        return super().non_db_attrs + ("sanitizer", "sanitizer_name")

    def pre_save(self, model_instance: models.Model, add: bool) -> str:
        value = self.sanitizer.sanitize(super().pre_save(model_instance, add))
        setattr(model_instance, self.attname, value)
        return value
