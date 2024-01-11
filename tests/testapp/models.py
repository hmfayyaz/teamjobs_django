from django.db import models

from api.fields import CleanHTMLField


class HtmlFieldModel(models.Model):
    html_field = CleanHTMLField()
    html_field_invalid_sanitizier = CleanHTMLField(sanitizer="nonexistant", default="")
    html_field_with_sanitizer = CleanHTMLField(
        sanitizer="testapp_sanitizer", default=""
    )
