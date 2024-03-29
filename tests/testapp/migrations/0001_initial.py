# Generated by Django 4.2 on 2023-04-03 14:50

import api.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="HtmlFieldModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("html_field", api.fields.CleanHTMLField()),
                (
                    "html_field_invalid_sanitizier",
                    api.fields.CleanHTMLField(default="", sanitizer="nonexistant"),
                ),
                (
                    "html_field_with_sanitizer",
                    api.fields.CleanHTMLField(
                        default="", sanitizer="testapp_sanitizer"
                    ),
                ),
            ],
        ),
    ]
