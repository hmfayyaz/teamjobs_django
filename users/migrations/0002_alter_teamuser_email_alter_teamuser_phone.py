# Generated by Django 4.1.6 on 2023-02-12 00:03

import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="teamuser",
            name="email",
            field=models.EmailField(max_length=254, unique=True, verbose_name="email"),
        ),
        migrations.AlterField(
            model_name="teamuser",
            name="phone",
            field=phonenumber_field.modelfields.PhoneNumberField(
                blank=True, max_length=128, region=None, verbose_name="phone number"
            ),
        ),
    ]