# Generated by Django 4.1.7 on 2023-03-28 17:36

from django.db import migrations
import django_jsonform.models.fields


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0014_rename_address_business_address_old"),
    ]

    operations = [
        migrations.AddField(
            model_name="business",
            name="address",
            field=django_jsonform.models.fields.JSONField(
                default=dict, verbose_name="address"
            ),
        ),
    ]
